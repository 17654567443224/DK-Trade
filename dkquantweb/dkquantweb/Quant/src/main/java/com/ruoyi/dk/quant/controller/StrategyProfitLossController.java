package com.ruoyi.dk.quant.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

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
import com.ruoyi.dk.quant.domain.StrategyProfitLoss;
import com.ruoyi.dk.quant.service.IStrategyProfitLossService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 止盈止损策略Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "止盈止损策略相关接口")
@RestController
@RequestMapping("/strategy/strategy_profitLoss")
public class StrategyProfitLossController extends BaseController
{
    @Autowired
    private IStrategyProfitLossService strategyProfitLossService;

    /**
     * 查询止盈止损策略列表
     */
    @ApiOperation(value = "查询止盈止损策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_profitLoss:list')")
    @GetMapping("/list")
    public TableDataInfo list(StrategyProfitLoss strategyProfitLoss)
    {
        startPage();
        List<StrategyProfitLoss> list = strategyProfitLossService.selectStrategyProfitLossList(strategyProfitLoss);
        return getDataTable(list);
    }

    /**
     * 导出止盈止损策略列表
     */
    @ApiOperation(value = "导出止盈止损策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_profitLoss:export')")
    @Log(title = "止盈止损策略", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategyProfitLoss strategyProfitLoss)
    {
        List<StrategyProfitLoss> list = strategyProfitLossService.selectStrategyProfitLossList(strategyProfitLoss);
        ExcelUtil<StrategyProfitLoss> util = new ExcelUtil<StrategyProfitLoss>(StrategyProfitLoss.class);
        util.exportExcel(response, list, "止盈止损策略数据");
    }

    /**
     * 获取止盈止损策略详细信息
     */
    @ApiOperation(value = "获取止盈止损策略详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_profitLoss:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyProfitLossService.selectStrategyProfitLossById(id));
    }

    /**
     * 新增止盈止损策略
     */
    @ApiOperation(value = "新增止盈止损策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_profitLoss:add')")
    @Log(title = "止盈止损策略", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyProfitLoss strategyProfitLoss)
    {
        strategyProfitLossService.insertStrategyProfitLoss(strategyProfitLoss);
        return success(strategyProfitLoss.getId());
    }

    /**
     * 修改止盈止损策略
     */
    @ApiOperation(value = "修改止盈止损策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_profitLoss:edit')")
    @Log(title = "止盈止损策略", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyProfitLoss strategyProfitLoss)
    {
        return toAjax(strategyProfitLossService.updateStrategyProfitLoss(strategyProfitLoss));
    }

    /**
     * 删除止盈止损策略
     */
    @ApiOperation(value = "删除止盈止损策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_profitLoss:remove')")
    @Log(title = "止盈止损策略", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyProfitLossService.deleteStrategyProfitLossByIds(ids));
    }
}
