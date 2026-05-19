package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.StrategyFund;

/**
 * 资金策略Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface StrategyFundMapper 
{
    /**
     * 查询资金策略
     * 
     * @param id 资金策略主键
     * @return 资金策略
     */
    public StrategyFund selectStrategyFundById(Long id);

    /**
     * 查询资金策略列表
     * 
     * @param strategyFund 资金策略
     * @return 资金策略集合
     */
    public List<StrategyFund> selectStrategyFundList(StrategyFund strategyFund);

    /**
     * 新增资金策略
     * 
     * @param strategyFund 资金策略
     * @return 结果
     */
    public int insertStrategyFund(StrategyFund strategyFund);

    /**
     * 修改资金策略
     * 
     * @param strategyFund 资金策略
     * @return 结果
     */
    public int updateStrategyFund(StrategyFund strategyFund);

    /**
     * 删除资金策略
     * 
     * @param id 资金策略主键
     * @return 结果
     */
    public int deleteStrategyFundById(Long id);

    /**
     * 批量删除资金策略
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategyFundByIds(Long[] ids);
}
