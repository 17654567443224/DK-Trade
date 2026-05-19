package com.ruoyi.dk.quant.service;

import com.ruoyi.dk.quant.domain.StrategyGenerateReport;

import java.util.List;


/**
 * 策略绩效指标Service接口
 * 
 * @author ruoyi
 * @date 2025-02-15
 */
public interface IStrategyGenerateReportService 
{
    /**
     * 查询策略绩效指标
     * 
     * @param id 策略绩效指标主键
     * @return 策略绩效指标
     */
    public StrategyGenerateReport selectStrategyGenerateReportById(Long id);

    /**
     * 查询策略绩效指标列表
     * 
     * @param strategyGenerateReport 策略绩效指标
     * @return 策略绩效指标集合
     */
    public List<StrategyGenerateReport> selectStrategyGenerateReportList(StrategyGenerateReport strategyGenerateReport);

    /**
     * 新增策略绩效指标
     * 
     * @param strategyGenerateReport 策略绩效指标
     * @return 结果
     */
    public int insertStrategyGenerateReport(StrategyGenerateReport strategyGenerateReport);

    /**
     * 修改策略绩效指标
     * 
     * @param strategyGenerateReport 策略绩效指标
     * @return 结果
     */
    public int updateStrategyGenerateReport(StrategyGenerateReport strategyGenerateReport);

    /**
     * 批量删除策略绩效指标
     * 
     * @param ids 需要删除的策略绩效指标主键集合
     * @return 结果
     */
    public int deleteStrategyGenerateReportByIds(Long[] ids);

    /**
     * 删除策略绩效指标信息
     * 
     * @param id 策略绩效指标主键
     * @return 结果
     */
    public int deleteStrategyGenerateReportById(Long id);
}
