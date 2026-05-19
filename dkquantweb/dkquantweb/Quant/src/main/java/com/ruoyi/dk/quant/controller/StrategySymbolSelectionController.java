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
import com.ruoyi.dk.quant.domain.StrategySymbolSelection;
import com.ruoyi.dk.quant.service.IStrategySymbolSelectionService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 选股策略Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "选股策略相关接口")
@RestController
@RequestMapping("/strategy/strategy_selection")
public class StrategySymbolSelectionController extends BaseController
{
    @Autowired
    private IStrategySymbolSelectionService strategySymbolSelectionService;

    /**
     * 查询选股策略列表
     */
    @ApiOperation(value = "查询选股策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_selection:list')")
    @GetMapping("/list")
    public TableDataInfo list(StrategySymbolSelection strategySymbolSelection)
    {
        startPage();
        List<StrategySymbolSelection> list = strategySymbolSelectionService.selectStrategySymbolSelectionList(strategySymbolSelection);
        return getDataTable(list);
    }

    /**
     * 导出选股策略列表
     */
    @ApiOperation(value = "导出选股策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_selection:export')")
    @Log(title = "选股策略", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategySymbolSelection strategySymbolSelection)
    {
        List<StrategySymbolSelection> list = strategySymbolSelectionService.selectStrategySymbolSelectionList(strategySymbolSelection);
        ExcelUtil<StrategySymbolSelection> util = new ExcelUtil<StrategySymbolSelection>(StrategySymbolSelection.class);
        util.exportExcel(response, list, "选股策略数据");
    }

    /**
     * 获取选股策略详细信息
     */
    @ApiOperation(value = "获取选股策略详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_selection:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategySymbolSelectionService.selectStrategySymbolSelectionById(id));
    }

    /**
     * 新增选股策略
     */
    @ApiOperation(value = "新增选股策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_selection:add')")
    @Log(title = "选股策略", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategySymbolSelection strategySymbolSelection)
    {
        strategySymbolSelectionService.insertStrategySymbolSelection(strategySymbolSelection);
        return success(strategySymbolSelection.getId());
    }

    /**
     * 修改选股策略
     */
    @ApiOperation(value = "修改选股策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_selection:edit')")
    @Log(title = "选股策略", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategySymbolSelection strategySymbolSelection)
    {
        return toAjax(strategySymbolSelectionService.updateStrategySymbolSelection(strategySymbolSelection));
    }

    /**
     * 删除选股策略
     */
    @ApiOperation(value = "删除选股策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_selection:remove')")
    @Log(title = "选股策略", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategySymbolSelectionService.deleteStrategySymbolSelectionByIds(ids));
    }
}
