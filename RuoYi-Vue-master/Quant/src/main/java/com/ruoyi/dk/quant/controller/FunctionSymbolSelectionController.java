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
import com.ruoyi.dk.quant.domain.FunctionSymbolSelection;
import com.ruoyi.dk.quant.service.IFunctionSymbolSelectionService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 选股方法Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "选股方法相关接口")
@RestController
@RequestMapping("/strategy/fun_selection")
public class FunctionSymbolSelectionController extends BaseController
{
    @Autowired
    private IFunctionSymbolSelectionService functionSymbolSelectionService;

    /**
     * 查询选股方法列表
     */
    @ApiOperation(value = "查询选股方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_selection:list')")
    @GetMapping("/list")
    public TableDataInfo list(FunctionSymbolSelection functionSymbolSelection)
    {
        startPage();
        List<FunctionSymbolSelection> list = functionSymbolSelectionService.selectFunctionSymbolSelectionList(functionSymbolSelection);
        return getDataTable(list);
    }

    /**
     * 导出选股方法列表
     */
    @ApiOperation(value = "导出选股方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_selection:export')")
    @Log(title = "选股方法", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, FunctionSymbolSelection functionSymbolSelection)
    {
        List<FunctionSymbolSelection> list = functionSymbolSelectionService.selectFunctionSymbolSelectionList(functionSymbolSelection);
        ExcelUtil<FunctionSymbolSelection> util = new ExcelUtil<FunctionSymbolSelection>(FunctionSymbolSelection.class);
        util.exportExcel(response, list, "选股方法数据");
    }

    /**
     * 获取选股方法详细信息
     */
    @ApiOperation(value = "获取选股方法详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:fun_selection:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(functionSymbolSelectionService.selectFunctionSymbolSelectionById(id));
    }

    /**
     * 新增选股方法
     */
    @ApiOperation(value = "新增选股方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_selection:add')")
    @Log(title = "选股方法", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody FunctionSymbolSelection functionSymbolSelection)
    {
        functionSymbolSelectionService.insertFunctionSymbolSelection(functionSymbolSelection);
        return success(functionSymbolSelection.getId());
    }

    /**
     * 修改选股方法
     */
    @ApiOperation(value = "修改选股方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_selection:edit')")
    @Log(title = "选股方法", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody FunctionSymbolSelection functionSymbolSelection)
    {
        return toAjax(functionSymbolSelectionService.updateFunctionSymbolSelection(functionSymbolSelection));
    }

    /**
     * 删除选股方法
     */
    @ApiOperation(value = "删除选股方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_selection:remove')")
    @Log(title = "选股方法", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(functionSymbolSelectionService.deleteFunctionSymbolSelectionByIds(ids));
    }
}
