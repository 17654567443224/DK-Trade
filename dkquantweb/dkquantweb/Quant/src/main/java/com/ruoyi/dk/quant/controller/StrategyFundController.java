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
import com.ruoyi.dk.quant.domain.StrategyFund;
import com.ruoyi.dk.quant.service.IStrategyFundService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 资金策略Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "资金策略相关接口")
@RestController
@RequestMapping("/strategy/strategy_fund")
public class StrategyFundController extends BaseController
{
    @Autowired
    private IStrategyFundService strategyFundService;

    /**
     * 查询资金策略列表
     */
    @ApiOperation(value = "查询资金策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_fund:list')")
    @GetMapping("/list")
    public TableDataInfo list(StrategyFund strategyFund)
    {
        startPage();
        List<StrategyFund> list = strategyFundService.selectStrategyFundList(strategyFund);
        return getDataTable(list);
    }

    /**
     * 导出资金策略列表
     */
    @ApiOperation(value = "导出资金策略列表")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_fund:export')")
    @Log(title = "资金策略", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategyFund strategyFund)
    {
        List<StrategyFund> list = strategyFundService.selectStrategyFundList(strategyFund);
        ExcelUtil<StrategyFund> util = new ExcelUtil<StrategyFund>(StrategyFund.class);
        util.exportExcel(response, list, "资金策略数据");
    }

    /**
     * 获取资金策略详细信息
     */
    @ApiOperation(value = "获取资金策略详细信息")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_fund:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyFundService.selectStrategyFundById(id));
    }

    /**
     * 新增资金策略
     */
    @ApiOperation(value = "新增资金策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_fund:add')")
    @Log(title = "资金策略", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyFund strategyFund)
    {
        strategyFundService.insertStrategyFund(strategyFund);
        return success(strategyFund.getId());
    }

    /**
     * 修改资金策略
     */
    @ApiOperation(value = "修改资金策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_fund:edit')")
    @Log(title = "资金策略", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyFund strategyFund)
    {
        return toAjax(strategyFundService.updateStrategyFund(strategyFund));
    }

    /**
     * 删除资金策略
     */
    @ApiOperation(value = "删除资金策略")
    @PreAuthorize("@ss.hasPermi('strategy:strategy_fund:remove')")
    @Log(title = "资金策略", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyFundService.deleteStrategyFundByIds(ids));
    }
}
