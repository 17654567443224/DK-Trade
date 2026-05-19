package com.ruoyi.dk.quant.service.impl;

import java.util.List;

import com.ruoyi.dk.quant.domain.StrategyGenerateReport;
import com.ruoyi.dk.quant.mapper.StrategyGenerateReportMapper;
import com.ruoyi.dk.quant.service.IStrategyGenerateReportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


/**
 * 策略绩效指标Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-15
 */
@Service
public class StrategyGenerateReportServiceImpl implements IStrategyGenerateReportService
{
    @Autowired
    private StrategyGenerateReportMapper strategyGenerateReportMapper;

    /**
     * 查询策略绩效指标
     * 
     * @param id 策略绩效指标主键
     * @return 策略绩效指标
     */
    @Override
    public StrategyGenerateReport selectStrategyGenerateReportById(Long id)
    {
        return strategyGenerateReportMapper.selectStrategyGenerateReportById(id);
    }

    /**
     * 查询策略绩效指标列表
     * 
     * @param strategyGenerateReport 策略绩效指标
     * @return 策略绩效指标
     */
    @Override
    public List<StrategyGenerateReport> selectStrategyGenerateReportList(StrategyGenerateReport strategyGenerateReport)
    {
        return strategyGenerateReportMapper.selectStrategyGenerateReportList(strategyGenerateReport);
    }

    /**
     * 新增策略绩效指标
     * 
     * @param strategyGenerateReport 策略绩效指标
     * @return 结果
     */
    @Override
    public int insertStrategyGenerateReport(StrategyGenerateReport strategyGenerateReport)
    {
        return strategyGenerateReportMapper.insertStrategyGenerateReport(strategyGenerateReport);
    }

    /**
     * 修改策略绩效指标
     * 
     * @param strategyGenerateReport 策略绩效指标
     * @return 结果
     */
    @Override
    public int updateStrategyGenerateReport(StrategyGenerateReport strategyGenerateReport)
    {
        return strategyGenerateReportMapper.updateStrategyGenerateReport(strategyGenerateReport);
    }

    /**
     * 批量删除策略绩效指标
     * 
     * @param ids 需要删除的策略绩效指标主键
     * @return 结果
     */
    @Override
    public int deleteStrategyGenerateReportByIds(Long[] ids)
    {
        return strategyGenerateReportMapper.deleteStrategyGenerateReportByIds(ids);
    }

    /**
     * 删除策略绩效指标信息
     * 
     * @param id 策略绩效指标主键
     * @return 结果
     */
    @Override
    public int deleteStrategyGenerateReportById(Long id)
    {
        return strategyGenerateReportMapper.deleteStrategyGenerateReportById(id);
    }
}
