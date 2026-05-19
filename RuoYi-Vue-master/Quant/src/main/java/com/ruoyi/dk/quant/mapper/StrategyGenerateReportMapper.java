package com.ruoyi.dk.quant.mapper;

import com.ruoyi.dk.quant.domain.StrategyGenerateReport;

import java.util.List;


/**
 * 策略绩效指标Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-15
 */
public interface StrategyGenerateReportMapper 
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
     * 删除策略绩效指标
     * 
     * @param id 策略绩效指标主键
     * @return 结果
     */
    public int deleteStrategyGenerateReportById(Long id);

    /**
     * 批量删除策略绩效指标
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategyGenerateReportByIds(Long[] ids);
}
