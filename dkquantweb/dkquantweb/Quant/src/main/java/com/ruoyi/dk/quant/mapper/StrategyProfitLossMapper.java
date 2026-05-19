package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.StrategyProfitLoss;

/**
 * 止盈止损策略Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface StrategyProfitLossMapper 
{
    /**
     * 查询止盈止损策略
     * 
     * @param id 止盈止损策略主键
     * @return 止盈止损策略
     */
    public StrategyProfitLoss selectStrategyProfitLossById(Long id);

    /**
     * 查询止盈止损策略列表
     * 
     * @param strategyProfitLoss 止盈止损策略
     * @return 止盈止损策略集合
     */
    public List<StrategyProfitLoss> selectStrategyProfitLossList(StrategyProfitLoss strategyProfitLoss);

    /**
     * 新增止盈止损策略
     * 
     * @param strategyProfitLoss 止盈止损策略
     * @return 结果
     */
    public int insertStrategyProfitLoss(StrategyProfitLoss strategyProfitLoss);

    /**
     * 修改止盈止损策略
     * 
     * @param strategyProfitLoss 止盈止损策略
     * @return 结果
     */
    public int updateStrategyProfitLoss(StrategyProfitLoss strategyProfitLoss);

    /**
     * 删除止盈止损策略
     * 
     * @param id 止盈止损策略主键
     * @return 结果
     */
    public int deleteStrategyProfitLossById(Long id);

    /**
     * 批量删除止盈止损策略
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategyProfitLossByIds(Long[] ids);
}
