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
import com.ruoyi.dk.quant.domain.StrategyOpenPosition;
import com.ruoyi.dk.quant.service.IStrategyOpenPositionService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 开仓策略Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "开仓策略相关接口")
@RestController
@RequestMapping("/strategy/strategy_position")
public class StrategyOpenPositionController extends BaseController
{
    @Autowired
    private IStrategyOpenPositionService strategyOpenPositionService;

    /**
     * 查询开仓策略列表
     */
    @ApiOperation(value = "查询开仓策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_position:list')")
    @GetMapping("/list")
    public TableDataInfo list(StrategyOpenPosition strategyOpenPosition)
    {
        startPage();
        List<StrategyOpenPosition> list = strategyOpenPositionService.selectStrategyOpenPositionList(strategyOpenPosition);
        return getDataTable(list);
    }

    /**
     * 导出开仓策略列表
     */
    @ApiOperation(value = "导出开仓策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_position:export')")
    @Log(title = "开仓策略", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategyOpenPosition strategyOpenPosition)
    {
        List<StrategyOpenPosition> list = strategyOpenPositionService.selectStrategyOpenPositionList(strategyOpenPosition);
        ExcelUtil<StrategyOpenPosition> util = new ExcelUtil<StrategyOpenPosition>(StrategyOpenPosition.class);
        util.exportExcel(response, list, "开仓策略数据");
    }

    /**
     * 获取开仓策略详细信息
     */
    @ApiOperation(value = "获取开仓策略详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_position:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyOpenPositionService.selectStrategyOpenPositionById(id));
    }

    /**
     * 新增开仓策略
     */
    @ApiOperation(value = "新增开仓策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_position:add')")
    @Log(title = "开仓策略", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyOpenPosition strategyOpenPosition)
    {
        strategyOpenPositionService.insertStrategyOpenPosition(strategyOpenPosition);
        return success(strategyOpenPosition.getId());
    }

    /**
     * 修改开仓策略
     */
    @ApiOperation(value = "修改开仓策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_position:edit')")
    @Log(title = "开仓策略", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyOpenPosition strategyOpenPosition)
    {
        return toAjax(strategyOpenPositionService.updateStrategyOpenPosition(strategyOpenPosition));
    }

    /**
     * 删除开仓策略
     */
    @ApiOperation(value = "删除开仓策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_position:remove')")
    @Log(title = "开仓策略", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyOpenPositionService.deleteStrategyOpenPositionByIds(ids));
    }
}
