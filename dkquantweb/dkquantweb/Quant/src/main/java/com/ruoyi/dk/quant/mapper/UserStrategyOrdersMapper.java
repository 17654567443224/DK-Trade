package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.UserStrategyOrders;

/**
 * 策略订单信息Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface UserStrategyOrdersMapper 
{
    /**
     * 查询策略订单信息
     * 
     * @param id 策略订单信息主键
     * @return 策略订单信息
     */
    public UserStrategyOrders selectUserStrategyOrdersById(Long id);

    /**
     * 查询策略订单信息列表
     * 
     * @param userStrategyOrders 策略订单信息
     * @return 策略订单信息集合
     */
    public List<UserStrategyOrders> selectUserStrategyOrdersList(UserStrategyOrders userStrategyOrders);

    /**
     * 新增策略订单信息
     * 
     * @param userStrategyOrders 策略订单信息
     * @return 结果
     */
    public int insertUserStrategyOrders(UserStrategyOrders userStrategyOrders);

    /**
     * 修改策略订单信息
     * 
     * @param userStrategyOrders 策略订单信息
     * @return 结果
     */
    public int updateUserStrategyOrders(UserStrategyOrders userStrategyOrders);

    /**
     * 删除策略订单信息
     * 
     * @param id 策略订单信息主键
     * @return 结果
     */
    public int deleteUserStrategyOrdersById(Long id);

    /**
     * 批量删除策略订单信息
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteUserStrategyOrdersByIds(Long[] ids);
}
