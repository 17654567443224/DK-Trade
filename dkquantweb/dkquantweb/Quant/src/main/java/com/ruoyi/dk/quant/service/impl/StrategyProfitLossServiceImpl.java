package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategyProfitLossMapper;
import com.ruoyi.dk.quant.domain.StrategyProfitLoss;
import com.ruoyi.dk.quant.service.IStrategyProfitLossService;

/**
 * 止盈止损策略Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class StrategyProfitLossServiceImpl implements IStrategyProfitLossService 
{
    @Autowired
    private StrategyProfitLossMapper strategyProfitLossMapper;

    /**
     * 查询止盈止损策略
     * 
     * @param id 止盈止损策略主键
     * @return 止盈止损策略
     */
    @Override
    public StrategyProfitLoss selectStrategyProfitLossById(Long id)
    {
        return strategyProfitLossMapper.selectStrategyProfitLossById(id);
    }

    /**
     * 查询止盈止损策略列表
     * 
     * @param strategyProfitLoss 止盈止损策略
     * @return 止盈止损策略
     */
    @Override
    public List<StrategyProfitLoss> selectStrategyProfitLossList(StrategyProfitLoss strategyProfitLoss)
    {
        return strategyProfitLossMapper.selectStrategyProfitLossList(strategyProfitLoss);
    }

    /**
     * 新增止盈止损策略
     * 
     * @param strategyProfitLoss 止盈止损策略
     * @return 结果
     */
    @Override
    public int insertStrategyProfitLoss(StrategyProfitLoss strategyProfitLoss)
    {
        return strategyProfitLossMapper.insertStrategyProfitLoss(strategyProfitLoss);
    }

    /**
     * 修改止盈止损策略
     * 
     * @param strategyProfitLoss 止盈止损策略
     * @return 结果
     */
    @Override
    public int updateStrategyProfitLoss(StrategyProfitLoss strategyProfitLoss)
    {
        return strategyProfitLossMapper.updateStrategyProfitLoss(strategyProfitLoss);
    }

    /**
     * 批量删除止盈止损策略
     * 
     * @param ids 需要删除的止盈止损策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyProfitLossByIds(Long[] ids)
    {
        return strategyProfitLossMapper.deleteStrategyProfitLossByIds(ids);
    }

    /**
     * 删除止盈止损策略信息
     * 
     * @param id 止盈止损策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyProfitLossById(Long id)
    {
        return strategyProfitLossMapper.deleteStrategyProfitLossById(id);
    }
}
