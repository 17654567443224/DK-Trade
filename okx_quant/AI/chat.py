import time
import numpy as np
import pymysql
from dtw import accelerated_dtw
from functionns.utils import deal_message
import okx.Market_api as Market
from threading import Thread, Lock
marketAPI = Market.MarketAPI(True)
def normalize_kline_data(kline):
    """归一化K线数据"""
    return (kline - np.min(kline, axis=0)) / (np.max(kline, axis=0) - np.min(kline, axis=0))

def batch_kline(intervals, symbol, ts):
    # 创建固定大小的结果列表
    ls = [None] * 5
    lock = Lock()
    count = 0

    # 根据 interval 设置 count
    if intervals == "15m":
        count = 900000
    elif intervals == "1H":
        count = 900000 * 4
    elif intervals == "4H":
        count = 900000 * 4 * 4
    ts = int(ts)
    # 计算不同的时间戳
    ts_list = [ts + count * i * 100 for i in range(5)]

    # 创建线程
    threads = []
    for i, ts_i in enumerate(ts_list):
        t = Thread(target=pred_from_kline, args=(symbol, intervals, ts_i, ls, i, lock, "100"))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 返回有序结果
    return ls
def pred_from_kline(symbol, intervals, ts, ls, index, lock, limit):
    while True:
        try:
            Kline_4h = marketAPI.get_markprice_candlesticks(instId=symbol, bar=intervals, after=ts, limit=limit)
            code = Kline_4h.get('code')
            if code == '0':
                all_res = deal_message(Kline_4h)
                all_res = [tuple(i[1:-1]) for i in all_res]
                with lock:  # 确保对 ls 的操作是线程安全的
                    ls[index] = all_res
                    break
            else:
                print(Kline_4h)
                continue
        except Exception as e:
            time.sleep(2)
            print("pred_from_kline:" + str(e))
            continue

def get_kline_data_from_api(limit, symbol, interval, ts):
    data = batch_kline(intervals=interval, symbol=symbol, ts=ts)
    Kl_dt = [dts for i in data for dts in i]
    dt = Kl_dt[:limit]

    kline_data = np.array(dt, dtype=np.float64)
    return kline_data


def get_kline_data_from_db(host, user, password, database, table_name, limit=None):
    """从数据库中读取K线数据"""
    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        with connection.cursor() as cursor:
            if limit:
                query = f"""
                    SELECT `open`, `high`, `low`, `close` 
                    FROM `{table_name}` 
                    ORDER BY `id` DESC 
                    LIMIT {limit}
                """
                cursor.execute(query)
                data = cursor.fetchall()
                data = data[::-1]  # 将数据反转为升序
            else:
                query = f"SELECT `open`, `high`, `low`, `close` FROM `{table_name}` ORDER BY `id` ASC"
                cursor.execute(query)
                data = cursor.fetchall()

            kline_data = np.array(data, dtype=np.float64)
    except pymysql.MySQLError as e:
        print(f"数据库连接错误：{e}")
        return np.array([])  # 返回空数组以避免程序中断
    finally:
        if connection:
            connection.close()
    return kline_data

def compare_segments(segment1, segment2, dtw_distances=None, max_length_diff=0.25, dynamic_percentile=90):
    """比较两段K线数据的相似性"""
    len1, len2 = len(segment1), len(segment2)
    if abs(len1 - len2) / max(len1, len2) > max_length_diff:
        return False, None

    if segment1 is None or segment2 is None or len(segment1) == 0 or len(segment2) == 0:
        return False, None
    if np.all(segment1 == segment1[0]) or np.all(segment2 == segment2[0]):
        return False, None

    dist, _, _, _ = accelerated_dtw(segment1, segment2, dist='euclidean')
    if dist is None or np.isnan(dist):
        return False, None

    if dtw_distances and len(dtw_distances) > 0:
        valid_distances = [d for d in dtw_distances if d is not None and not np.isnan(d)]
        similarity_threshold = np.percentile(valid_distances, dynamic_percentile) if valid_distances else 0.1
    else:
        similarity_threshold = 0.1

    return dist < similarity_threshold, dist

def find_patterns_with_gap(data, original_length, max_range, step=50, max_gap_ratio=0.1, dynamic_percentile=90):
    """寻找规律（允许间隔，动态调整阈值）"""
    original_segment = data[:original_length]
    max_gap = int(original_length * max_gap_ratio)
    patterns = []
    dtw_distances = []

    for start in range(original_length + max_gap, min(max_range, len(data) - step), step):
        for end in range(start + step, min(max_range, len(data) + 1), step):
            comparison_segment = data[start:end]
            is_similar, dist = compare_segments(
                original_segment,
                comparison_segment,
                dtw_distances=dtw_distances,
                dynamic_percentile=dynamic_percentile
            )
            if dist is not None and not np.isnan(dist):
                dtw_distances.append(dist)
            if is_similar:
                patterns.append({
                    'original_segment': (0, original_length),
                    'comparison_segment': (start, end),
                    'similarity': dist
                })

    return patterns

def find_all_patterns(data, initial_length=20, max_step=5):
    """自动扩展原始数据段长度，寻找所有规律"""
    total_length = len(data)
    max_original_length = total_length // 2
    all_patterns = []

    current_length = initial_length
    while current_length <= max_original_length:
        # print(f"正在处理原始数据段长度: {current_length}")
        patterns = find_patterns_with_gap(
            data,
            original_length=current_length,
            max_range=total_length,
            step=30
        )
        all_patterns.extend(patterns)
        current_length += max_step

    return all_patterns

def predict_future(data, patterns, predict_length=10):
    """根据找到的规律进行行情预测"""
    predictions = []
    epsilon = 1e-6

    for pattern in patterns:
        comparison_start, comparison_end = pattern['comparison_segment']
        similarity = pattern['similarity']

        future_start = comparison_end
        future_end = future_start + predict_length

        if future_end > len(data):
            continue

        future_segment = data[future_start:future_end, 3]  # 使用Close价格
        if future_segment[0] == 0:
            continue

        total_change = future_segment[-1] - future_segment[0]
        total_change_pct = total_change * 100  # 对归一化数据，直接计算百分比变化

        weight = 1 / (similarity + epsilon)

        predictions.append({
            'total_change': total_change,
            'total_change_pct': total_change_pct,
            'weight': weight,
            'similarity': similarity,
        })

    predictions.sort(key=lambda x: x['weight'], reverse=True)
    avg_similarity = np.mean([pred['similarity'] for pred in predictions]) if predictions else None

    return predictions, avg_similarity

def deal_predictions(predictions):
    res_detail = []
    #输出汇总结果
    for res in predictions:
        # print(f"表 {res['table']}，时间间隔 {res['interval']}，数据条数 {res['limit']}，预测结果：")

        # 收集相似度小于平均值的涨跌幅
        below_avg_changes = []
        # 初始化变量
        total_weighted_change_up = 0  # 涨的总加权变化
        total_weight_up = 0  # 涨的总权重
        total_weighted_change_down = 0  # 跌的总加权变化
        total_weight_down = 0  # 跌的总权重
        if not res['predictions']:
            continue
        # 遍历预测结果
        for pred in res['predictions']:
            change = pred['total_change']
            weight = pred['weight']

            if change > 0:  # 涨
                total_weighted_change_up += change * weight
                total_weight_up += weight
            elif change < 0:  # 跌
                total_weighted_change_down += change * weight
                total_weight_down += weight

        # 计算涨和跌的加权平均
        avg_change_up = total_weighted_change_up / total_weight_up if total_weight_up > 0 else 0
        avg_change_down = total_weighted_change_down / total_weight_down if total_weight_down > 0 else 0


        for i, pred in enumerate(res['predictions']):
            # print(f"  预测 {i + 1}: 总涨跌={pred['total_change']:.4f}, 涨跌幅={pred['total_change_pct']:.2f}%, "
            #       f"权重={pred['weight']:.4f}, 相似度={pred['similarity']:.4f}")

            # 筛选相似度小于平均相似度的涨跌幅
            if pred['similarity'] < res['avg_similarity']:
                below_avg_changes.append(pred['total_change'])

        # print(f"  平均相似度: {res['avg_similarity']:.4f}")

        # 添加到 res_detail
        res_detail.append(
            {
                'symbol': res['table'],
                'interval': res['interval'],
                'limit': res['limit'],
                'below_avg_changes': below_avg_changes,  # 存储筛选出的涨跌幅
                'avg_change_up': avg_change_up,
                'avg_change_down': avg_change_down
            }
        )
    return res_detail

def run(intervals, limits, data_src="api", db_info=None, tables=None, ts=None):
    """
    执行预测：遍历所有的interval、limit、数据库连接信息和表，返回预测结果。
    :param intervals: K线数据的时间间隔列表
    :param limits: 对应的每个表需要读取的K线数据条数
    :param db_info: 数据库连接信息，包括host, user, password, database
    :param tables: 数据库中表的名称列表
    :return: 汇总的所有预测结果
    """
    all_predictions = []
    res = []
    if data_src == "db":
        for interval, limit, table in zip(intervals, limits, tables):
            host = db_info['host']
            user = db_info['user']
            password = db_info['password']
            database = db_info['database']

            print(f"正在读取表 {table} 的数据，时间间隔: {interval}, 数据条数: {limit}")

            kline_data = get_kline_data_from_db(host, user, password, database, table, limit)

            if kline_data.shape[0] < limit:
                print(f"警告：数据库中只有 {kline_data.shape[0]} 条数据，少于请求的 {limit} 条。")

            attempt_limit_increase(all_predictions, interval, kline_data, limit, table, source="db", db_info=db_info)
        res = deal_predictions(all_predictions)
    elif data_src == "api":
        for interval, limit, table in zip(intervals, limits, tables):
            kline_data = get_kline_data_from_api(limit, tables, interval, ts)

            if kline_data.shape[0] < limit:
                print(f"警告：只有 {kline_data.shape[0]} 条数据，少于请求的 {limit} 条。")

            attempt_limit_increase(all_predictions, interval, kline_data, limit, table, source="api")
        res = deal_predictions(all_predictions)
    return res

def attempt_limit_increase(all_predictions, interval, kline_data, limit, table, source="db", db_info=None, ts=None):
    """
    处理 all_patterns 为空时，动态增加 limit 的逻辑，最多尝试 4 次。
    """
    max_attempts = 4
    attempt = 0

    while attempt < max_attempts:
        # 归一化处理
        kline_data_normalized = normalize_kline_data(kline_data)
        # 寻找所有规律
        all_patterns = find_all_patterns(kline_data_normalized, initial_length=20, max_step=5)

        if all_patterns:  # 如果找到规律，停止尝试
            predictions, avg_similarity = predict_future(kline_data_normalized, all_patterns)
            summary = {
                'interval': interval,
                'limit': limit,
                'table': table,
                'predictions': predictions,
                'avg_similarity': avg_similarity
            }
            all_predictions.append(summary)
            return  # 直接返回，不再尝试

        print(f"表 {table}，时间间隔 {interval}，数据条数 {limit} 没有找到规律，尝试增加 limit。")
        limit += 50
        attempt += 1

        # 重新获取数据
        if source == "db":
            host = db_info['host']
            user = db_info['user']
            password = db_info['password']
            database = db_info['database']
            kline_data = get_kline_data_from_db(host, user, password, database, table, limit)
        elif source == "api":
            Kline_data = get_kline_data_from_api(limit, table, interval, ts)


        if kline_data.shape[0] < limit:
            print(f"警告：即使增加 limit 到 {limit}，数据库中仍只有 {kline_data.shape[0]} 条数据。")
            break  # 数据不足，提前终止

    # 达到最大尝试次数后，未找到规律
    print(f"表 {table}，时间间隔 {interval}，尝试 {max_attempts} 次后仍未找到规律。")
    all_predictions.append({
        'interval': interval,
        'limit': limit,
        'table': table,
        'predictions': [],
        'avg_similarity': None
    })


#
# # 示例调用
# db_info = {
#     'host': "127.0.0.1",
#     'user': "root",
#     'password': "lxw2866",
#     'database': "market_data"
# }
#
# intervals = ["15m", "1h", "4h"]  # 时间间隔列表，可以是多个时间间隔
# limits = [200, 200, 200]  # 每次从数据库获取的K线数据条数
# tables = ["btcusdt_15m", "btcusdt_1h", "btcusdt_4h"]  # 表列表，可以是多个表
#
# # 执行预测
# a = run(intervals, limits, "db",db_info,  tables)
# print(a)



