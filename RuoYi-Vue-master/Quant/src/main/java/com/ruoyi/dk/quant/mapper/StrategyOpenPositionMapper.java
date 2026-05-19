package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.StrategyOpenPosition;

/**
 * 开仓策略Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface StrategyOpenPositionMapper 
{
    /**
     * 查询开仓策略
     * 
     * @param id 开仓策略主键
     * @return 开仓策略
     */
    public StrategyOpenPosition selectStrategyOpenPositionById(Long id);

    /**
     * 查询开仓策略列表
     * 
     * @param strategyOpenPosition 开仓策略
     * @return 开仓策略集合
     */
    public List<StrategyOpenPosition> selectStrategyOpenPositionList(StrategyOpenPosition strategyOpenPosition);

    /**
     * 新增开仓策略
     * 
     * @param strategyOpenPosition 开仓策略
     * @return 结果
     */
    public int insertStrategyOpenPosition(StrategyOpenPosition strategyOpenPosition);

    /**
     * 修改开仓策略
     * 
     * @param strategyOpenPosition 开仓策略
     * @return 结果
     */
    public int updateStrategyOpenPosition(StrategyOpenPosition strategyOpenPosition);

    /**
     * 删除开仓策略
     * 
     * @param id 开仓策略主键
     * @return 结果
     */
    public int deleteStrategyOpenPositionById(Long id);

    /**
     * 批量删除开仓策略
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategyOpenPositionByIds(Long[] ids);
}
