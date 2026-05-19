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
import com.ruoyi.dk.quant.domain.FunctionFund;
import com.ruoyi.dk.quant.service.IFunctionFundService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 资金方法Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "资金方法相关接口")
@RestController
@RequestMapping("/strategy/fun_fund")
public class FunctionFundController extends BaseController
{
    @Autowired
    private IFunctionFundService functionFundService;

    /**
     * 查询资金方法列表
     */
    @ApiOperation(value = "查询资金方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_fund:list')")
    @GetMapping("/list")
    public TableDataInfo list(FunctionFund functionFund)
    {
        startPage();
        List<FunctionFund> list = functionFundService.selectFunctionFundList(functionFund);
        return getDataTable(list);
    }

    /**
     * 导出资金方法列表
     */
    @ApiOperation(value = "导出资金方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_fund:export')")
    @Log(title = "资金方法", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, FunctionFund functionFund)
    {
        List<FunctionFund> list = functionFundService.selectFunctionFundList(functionFund);
        ExcelUtil<FunctionFund> util = new ExcelUtil<FunctionFund>(FunctionFund.class);
        util.exportExcel(response, list, "资金方法数据");
    }

    /**
     * 获取资金方法详细信息
     */
    @ApiOperation(value = "获取资金方法详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:fun_fund:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(functionFundService.selectFunctionFundById(id));
    }

    /**
     * 新增资金方法
     */
    @ApiOperation(value = "新增资金方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_fund:add')")
    @Log(title = "资金方法", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody FunctionFund functionFund)
    {
        functionFundService.insertFunctionFund(functionFund);
        return success(functionFund.getId());
    }

    /**
     * 修改资金方法
     */
    @ApiOperation(value = "修改资金方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_fund:edit')")
    @Log(title = "资金方法", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody FunctionFund functionFund)
    {
        return toAjax(functionFundService.updateFunctionFund(functionFund));
    }

    /**
     * 删除资金方法
     */
    @ApiOperation(value = "删除资金方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_fund:remove')")
    @Log(title = "资金方法", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(functionFundService.deleteFunctionFundByIds(ids));
    }
}
