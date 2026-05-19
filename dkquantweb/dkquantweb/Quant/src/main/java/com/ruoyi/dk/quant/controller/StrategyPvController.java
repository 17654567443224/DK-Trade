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
import com.ruoyi.dk.quant.domain.StrategyPv;
import com.ruoyi.dk.quant.service.IStrategyPvService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 私有策略Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "私有策略相关接口")
@RestController
@RequestMapping("/strategy/strategy_pv")
public class StrategyPvController extends BaseController
{
    @Autowired
    private IStrategyPvService strategyPvService;

    /**
     * 查询私有策略列表
     */
    @ApiOperation(value = "查询私有策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_pv:list')")
    @GetMapping("/list")
    public TableDataInfo list(StrategyPv strategyPv)
    {
        startPage();
        List<StrategyPv> list = strategyPvService.selectStrategyPvList(strategyPv);
        return getDataTable(list);
    }

    /**
     * 导出私有策略列表
     */
    @ApiOperation(value = "导出私有策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_pv:export')")
    @Log(title = "私有策略", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategyPv strategyPv)
    {
        List<StrategyPv> list = strategyPvService.selectStrategyPvList(strategyPv);
        ExcelUtil<StrategyPv> util = new ExcelUtil<StrategyPv>(StrategyPv.class);
        util.exportExcel(response, list, "私有策略数据");
    }

    /**
     * 获取私有策略详细信息
     */
    @ApiOperation(value = "获取私有策略详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_pv:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyPvService.selectStrategyPvById(id));
    }

    /**
     * 新增私有策略
     */
    @ApiOperation(value = "新增私有策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_pv:add')")
    @Log(title = "私有策略", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyPv strategyPv)
    {
        return toAjax(strategyPvService.insertStrategyPv(strategyPv));
    }

    /**
     * 修改私有策略
     */
    @ApiOperation(value = "修改私有策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_pv:edit')")
    @Log(title = "私有策略", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyPv strategyPv)
    {
        return toAjax(strategyPvService.updateStrategyPv(strategyPv));
    }

    /**
     * 删除私有策略
     */
    @ApiOperation(value = "删除私有策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_pv:remove')")
    @Log(title = "私有策略", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyPvService.deleteStrategyPvByIds(ids));
    }
}
