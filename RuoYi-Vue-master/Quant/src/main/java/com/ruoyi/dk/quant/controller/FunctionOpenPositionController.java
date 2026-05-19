package com.ruoyi.dk.quant.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModel;
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
import com.ruoyi.dk.quant.domain.FunctionOpenPosition;
import com.ruoyi.dk.quant.service.IFunctionOpenPositionService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 开仓方法Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "开仓方法相关接口")
@RestController
@RequestMapping("/strategy/fun_position")
public class FunctionOpenPositionController extends BaseController
{
    @Autowired
    private IFunctionOpenPositionService functionOpenPositionService;

    /**
     * 查询开仓方法列表
     */
    @ApiOperation(value = "查询开仓方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_position:list')")
    @GetMapping("/list")
    public TableDataInfo list(FunctionOpenPosition functionOpenPosition)
    {
        startPage();
        List<FunctionOpenPosition> list = functionOpenPositionService.selectFunctionOpenPositionList(functionOpenPosition);
        return getDataTable(list);
    }

    /**
     * 导出开仓方法列表
     */
    @ApiOperation(value = "导出开仓方法列表")
    @PreAuthorize("@ss.hasPermi('strategy:fun_position:export')")
    @Log(title = "开仓方法", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, FunctionOpenPosition functionOpenPosition)
    {
        List<FunctionOpenPosition> list = functionOpenPositionService.selectFunctionOpenPositionList(functionOpenPosition);
        ExcelUtil<FunctionOpenPosition> util = new ExcelUtil<FunctionOpenPosition>(FunctionOpenPosition.class);
        util.exportExcel(response, list, "开仓方法数据");
    }

    /**
     * 获取开仓方法详细信息
     */
    @ApiOperation(value = "获取开仓方法详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:fun_position:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(functionOpenPositionService.selectFunctionOpenPositionById(id));
    }

    /**
     * 新增开仓方法
     */
    @ApiOperation(value = "新增开仓方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_position:add')")
    @Log(title = "开仓方法", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody FunctionOpenPosition functionOpenPosition)
    {
        functionOpenPositionService.insertFunctionOpenPosition(functionOpenPosition);
        return success(functionOpenPosition.getId());
    }

    /**
     * 修改开仓方法
     */
    @ApiOperation(value = "修改开仓方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_position:edit')")
    @Log(title = "开仓方法", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody FunctionOpenPosition functionOpenPosition)
    {
        return toAjax(functionOpenPositionService.updateFunctionOpenPosition(functionOpenPosition));
    }

    /**
     * 删除开仓方法
     */
    @ApiOperation(value = "删除开仓方法")
    @PreAuthorize("@ss.hasPermi('strategy:fun_position:remove')")
    @Log(title = "开仓方法", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(functionOpenPositionService.deleteFunctionOpenPositionByIds(ids));
    }
}
