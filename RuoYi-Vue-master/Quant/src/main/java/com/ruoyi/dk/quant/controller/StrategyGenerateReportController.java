package com.ruoyi.dk.quant.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.ruoyi.dk.quant.domain.StrategyGenerateReport;
import com.ruoyi.dk.quant.service.IStrategyGenerateReportService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.enums.BusinessType;

import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 策略绩效指标Controller
 * 
 * @author ruoyi
 * @date 2025-02-15
 */
@Api(tags = "策略绩效指标相关接口")
@RestController
@RequestMapping("/system/report")
@PreAuthorize("@ss.hasRole('admin')")
public class StrategyGenerateReportController extends BaseController
{
    @Autowired
    private IStrategyGenerateReportService strategyGenerateReportService;

    /**
     * 查询策略绩效指标列表
     */
    @ApiOperation(value = "查询策略绩效指标列表")
    @GetMapping("/list")
    public TableDataInfo list(StrategyGenerateReport strategyGenerateReport)
    {
        startPage();
        List<StrategyGenerateReport> list = strategyGenerateReportService.selectStrategyGenerateReportList(strategyGenerateReport);
        return getDataTable(list);
    }

    /**
     * 导出策略绩效指标列表
     */
    @ApiOperation(value = "导出策略绩效指标列表")
    @PreAuthorize("@ss.hasPermi('system:report:export')")
    @Log(title = "策略绩效指标", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategyGenerateReport strategyGenerateReport)
    {
        List<StrategyGenerateReport> list = strategyGenerateReportService.selectStrategyGenerateReportList(strategyGenerateReport);
        ExcelUtil<StrategyGenerateReport> util = new ExcelUtil<StrategyGenerateReport>(StrategyGenerateReport.class);
        util.exportExcel(response, list, "策略绩效指标数据");
    }

    /**
     * 获取策略绩效指标详细信息
     */
    @ApiOperation(value = "获取策略绩效指标详细信息")
    @PreAuthorize("@ss.hasPermi('system:report:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyGenerateReportService.selectStrategyGenerateReportById(id));
    }

    /**
     * 新增策略绩效指标
     */
    @ApiOperation(value = "新增策略绩效指标")
    @PreAuthorize("@ss.hasPermi('system:report:add')")
    @Log(title = "策略绩效指标", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyGenerateReport strategyGenerateReport)
    {
        return toAjax(strategyGenerateReportService.insertStrategyGenerateReport(strategyGenerateReport));
    }

    /**
     * 修改策略绩效指标
     */
    @ApiOperation(value = "修改策略绩效指标")
    @PreAuthorize("@ss.hasPermi('system:report:edit')")
    @Log(title = "策略绩效指标", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyGenerateReport strategyGenerateReport)
    {
        return toAjax(strategyGenerateReportService.updateStrategyGenerateReport(strategyGenerateReport));
    }

    /**
     * 删除策略绩效指标
     */
    @ApiOperation(value = "删除策略绩效指标")
    @PreAuthorize("@ss.hasPermi('system:report:remove')")
    @Log(title = "策略绩效指标", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyGenerateReportService.deleteStrategyGenerateReportByIds(ids));
    }
}
