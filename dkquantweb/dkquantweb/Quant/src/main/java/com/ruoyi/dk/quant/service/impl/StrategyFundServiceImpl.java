package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategyFundMapper;
import com.ruoyi.dk.quant.domain.StrategyFund;
import com.ruoyi.dk.quant.service.IStrategyFundService;

/**
 * 资金策略Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class StrategyFundServiceImpl implements IStrategyFundService 
{
    @Autowired
    private StrategyFundMapper strategyFundMapper;

    /**
     * 查询资金策略
     * 
     * @param id 资金策略主键
     * @return 资金策略
     */
    @Override
    public StrategyFund selectStrategyFundById(Long id)
    {
        return strategyFundMapper.selectStrategyFundById(id);
    }

    /**
     * 查询资金策略列表
     * 
     * @param strategyFund 资金策略
     * @return 资金策略
     */
    @Override
    public List<StrategyFund> selectStrategyFundList(StrategyFund strategyFund)
    {
        return strategyFundMapper.selectStrategyFundList(strategyFund);
    }

    /**
     * 新增资金策略
     * 
     * @param strategyFund 资金策略
     * @return 结果
     */
    @Override
    public int insertStrategyFund(StrategyFund strategyFund)
    {
        return strategyFundMapper.insertStrategyFund(strategyFund);
    }

    /**
     * 修改资金策略
     * 
     * @param strategyFund 资金策略
     * @return 结果
     */
    @Override
    public int updateStrategyFund(StrategyFund strategyFund)
    {
        return strategyFundMapper.updateStrategyFund(strategyFund);
    }

    /**
     * 批量删除资金策略
     * 
     * @param ids 需要删除的资金策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyFundByIds(Long[] ids)
    {
        return strategyFundMapper.deleteStrategyFundByIds(ids);
    }

    /**
     * 删除资金策略信息
     * 
     * @param id 资金策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyFundById(Long id)
    {
        return strategyFundMapper.deleteStrategyFundById(id);
    }
}
