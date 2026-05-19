package com.ruoyi.dk.quant.service;

import java.util.List;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ruoyi.dk.quant.domain.BO.BackTestingBO;
import com.ruoyi.dk.quant.domain.BO.StrategyAddBO;
import com.ruoyi.dk.quant.domain.BO.StrategyBO;
import com.ruoyi.dk.quant.domain.Strategy;

/**
 * 策略Service接口
 * 
 * @author ruoyi
 * @date 2025-02-16
 */
public interface IStrategyService 
{
    /**
     * 查询策略
     * 
     * @param id 策略主键
     * @return 策略
     */
    public Strategy selectStrategyById(Long id);

    /**
     * 查询策略列表
     * 
     * @param strategy 策略
     * @return 策略集合
     */
    public List<Strategy> selectStrategyList(Strategy strategy);

    /**
     * 新增策略
     *
     * @param strategy 策略
     */
    public Long insertStrategy(StrategyAddBO strategy);

    /**
     * 修改策略
     * 
     * @param strategy 策略
     * @return 结果
     */
    public Long updateStrategy(StrategyAddBO strategy);

    /**
     * 批量删除策略
     * 
     * @param ids 需要删除的策略主键集合
     * @return 结果
     */
    public int deleteStrategyByIds(Long[] ids);

    /**
     * 删除策略信息
     * 
     * @param id 策略主键
     * @return 结果
     */
    public int deleteStrategyById(Long id);

    /**
     * 运行策略
     * @param strategyBO
     * @return
     */
    public String addStrategy(StrategyBO strategyBO) throws JsonProcessingException;

    public String runStrategy(StrategyBO strategyBO);

    public String removeStrategy(StrategyBO strategyBO);

    public Object operationInformation(StrategyBO strategyBO);

    public Object backTesting(BackTestingBO backTestingBO);

    public Object runningStrategies(StrategyBO strategyBO);

    public String initEngine();

    public String getOrders(StrategyBO strategyBO);

    public String getPositions(StrategyBO strategyBO);
}
