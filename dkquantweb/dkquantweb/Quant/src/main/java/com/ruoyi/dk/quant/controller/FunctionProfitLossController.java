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
import com.ruoyi.dk.quant.domain.FunctionProfitLoss;
import com.ruoyi.dk.quant.service.IFunctionProfitLossService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 止盈止损方法Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "止盈止损方法相关接口")
@RestController
@RequestMapping("/strategy/fun_profitLoss")
public class FunctionProfitLossController extends BaseController
{
    @Autowired
    private IFunctionProfitLossService functionProfitLossService;

    /**
     * 查询止盈止损方法列表
     */
    @ApiOperation(value = "查询止盈止损方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_profitLoss:list')")
    @GetMapping("/list")
    public TableDataInfo list(FunctionProfitLoss functionProfitLoss)
    {
        startPage();
        List<FunctionProfitLoss> list = functionProfitLossService.selectFunctionProfitLossList(functionProfitLoss);
        return getDataTable(list);
    }

    /**
     * 导出止盈止损方法列表
     */
    @ApiOperation(value = "导出止盈止损方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_profitLoss:export')")
    @Log(title = "止盈止损方法", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, FunctionProfitLoss functionProfitLoss)
    {
        List<FunctionProfitLoss> list = functionProfitLossService.selectFunctionProfitLossList(functionProfitLoss);
        ExcelUtil<FunctionProfitLoss> util = new ExcelUtil<FunctionProfitLoss>(FunctionProfitLoss.class);
        util.exportExcel(response, list, "止盈止损方法数据");
    }

    /**
     * 获取止盈止损方法详细信息
     */
    @ApiOperation(value = "获取止盈止损方法详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:fun_profitLoss:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(functionProfitLossService.selectFunctionProfitLossById(id));
    }

    /**
     * 新增止盈止损方法
     */
    @ApiOperation(value = "新增止盈止损方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_profitLoss:add')")
    @Log(title = "止盈止损方法", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody FunctionProfitLoss functionProfitLoss)
    {
        functionProfitLossService.insertFunctionProfitLoss(functionProfitLoss);
        return success(functionProfitLoss.getId());
    }

    /**
     * 修改止盈止损方法
     */
    @ApiOperation(value = "修改止盈止损方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_profitLoss:edit')")
    @Log(title = "止盈止损方法", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody FunctionProfitLoss functionProfitLoss)
    {
        return toAjax(functionProfitLossService.updateFunctionProfitLoss(functionProfitLoss));
    }

    /**
     * 删除止盈止损方法
     */
    @ApiOperation(value = "删除止盈止损方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_profitLoss:remove')")
    @Log(title = "止盈止损方法", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(functionProfitLossService.deleteFunctionProfitLossByIds(ids));
    }
}
