package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.StrategyPv;

/**
 * 私有策略Service接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface IStrategyPvService 
{
    /**
     * 查询私有策略
     * 
     * @param id 私有策略主键
     * @return 私有策略
     */
    public StrategyPv selectStrategyPvById(Long id);

    /**
     * 查询私有策略列表
     * 
     * @param strategyPv 私有策略
     * @return 私有策略集合
     */
    public List<StrategyPv> selectStrategyPvList(StrategyPv strategyPv);

    /**
     * 新增私有策略
     * 
     * @param strategyPv 私有策略
     * @return 结果
     */
    public int insertStrategyPv(StrategyPv strategyPv);

    /**
     * 修改私有策略
     * 
     * @param strategyPv 私有策略
     * @return 结果
     */
    public int updateStrategyPv(StrategyPv strategyPv);

    /**
     * 批量删除私有策略
     * 
     * @param ids 需要删除的私有策略主键集合
     * @return 结果
     */
    public int deleteStrategyPvByIds(Long[] ids);

    /**
     * 删除私有策略信息
     * 
     * @param id 私有策略主键
     * @return 结果
     */
    public int deleteStrategyPvById(Long id);
}
