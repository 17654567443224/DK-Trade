package com.ruoyi.dk.quant.controller;

import java.util.List;
import java.util.stream.Collectors;
import javax.servlet.http.HttpServletResponse;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.dk.quant.domain.BO.BackTestingBO;
import com.ruoyi.dk.quant.domain.BO.StrategyAddBO;
import com.ruoyi.dk.quant.domain.BO.StrategyBO;
import com.ruoyi.dk.quant.domain.RO.StrategyRO;
import com.ruoyi.dk.quant.utils.StrategyAddProcessor;
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
import com.ruoyi.dk.quant.domain.Strategy;
import com.ruoyi.dk.quant.service.IStrategyService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 策略Controller
 * 
 * @author ruoyi
 * @date 2025-02-16
 */
@Api(tags = "策略相关接口")
@RestController
@RequestMapping("/system/strategy")
public class StrategyController extends BaseController
{
    @Autowired
    private IStrategyService strategyService;

    @Autowired
    private StrategyAddProcessor strategyAddProcessor;

    /**
     * 查询策略列表
     */
    @ApiOperation(value = "查询策略列表")
    @PreAuthorize("@ss.hasPermi('system:strategy:list')")
    @GetMapping("/list")
    public TableDataInfo list(Strategy strategy)
    {
        startPage();
        List<Strategy> list = strategyService.selectStrategyList(strategy);
        List<StrategyRO> strategyROList = list.stream().map(strategyro -> {
            StrategyRO strategyRO = new StrategyRO();
            strategyRO.setStrategyName(strategyro.getStrategyName());
            strategyRO.setOwner(strategyro.getOwner());
            strategyRO.setLever(strategy.getLever());
            strategyRO.setId(strategyro.getId());
            strategyRO.setArgsId(strategyro.getArgsId());
            strategyRO.setMaxPosition(strategyro.getMaxPosition());
            return strategyRO;
        }).collect(Collectors.toList());
        return getDataTable(strategyROList);
    }

    /**
     * 导出策略列表
     */
    @ApiOperation(value = "导出策略列表")
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @Log(title = "策略", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Strategy strategy)
    {
        List<Strategy> list = strategyService.selectStrategyList(strategy);
        ExcelUtil<Strategy> util = new ExcelUtil<Strategy>(Strategy.class);
        util.exportExcel(response, list, "策略数据");
    }

    /**
     * 获取策略详细信息
     */
    @ApiOperation(value = "获取策略详细信息")
    @PreAuthorize("@ss.hasPermi('system:strategy:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyService.selectStrategyById(id));
    }

    /**
     * 新增策略
     */
    @ApiOperation(value = "新增策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:add')")
    @Log(title = "策略", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyAddBO strategyAddBO)
    {
        try {
            // 保存策略
            Long id = strategyService.insertStrategy(strategyAddBO);
            return success(id);
        } catch (Exception e) {
            e.printStackTrace();
            return AjaxResult.error("保存策略失败: " + e.getMessage());
        }
    }

    /**
     * 修改策略
     */
    @ApiOperation(value = "修改策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:edit')")
    @Log(title = "策略", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyAddBO strategyAddBO)
    {
        try {
            Long id = strategyService.updateStrategy(strategyAddBO);
            return success(id);
        } catch (Exception e){
            e.printStackTrace();
            return AjaxResult.error("修改策略失败: " + e.getMessage());
        }
    }

    /**
     * 删除策略
     */
    @ApiOperation(value = "删除策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:remove')")
    @Log(title = "策略", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyService.deleteStrategyByIds(ids));
    }

    /**
     * 初始化引擎
     */
    @ApiOperation(value = "初始化引擎")
    @PreAuthorize("@ss.hasAnyRoles('admin')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @GetMapping("/initEngine")
    public AjaxResult initEngine()
    {
        return success(strategyService.initEngine());
    }

    /**
     * 添加策略
     */
    @ApiOperation(value = "添加策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:addstrategy')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/addStrategy")
    public AjaxResult addStrategy(@RequestBody StrategyBO strategyBO) throws JsonProcessingException {
        return success(strategyService.addStrategy(strategyBO));
    }

    /**
     * 运行策略
     */
    @ApiOperation(value = "运行策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:run')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/runStrategy")
    public AjaxResult runStrategy(@RequestBody StrategyBO strategyBO)
    {
        return success(strategyService.runStrategy(strategyBO));
    }

    /**
     * 移除策略
     */
    @ApiOperation(value = "移除策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:removestrategy')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/removeStrategy")
    public AjaxResult removeStrategy(@RequestBody StrategyBO strategyBO)
    {
        return success(strategyService.removeStrategy(strategyBO));
    }

    /**
     * 获取绩效指标
     */
    @ApiOperation(value = "获取绩效指标")
    @PreAuthorize("@ss.hasPermi('system:strategy:operationinformation')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/operationInformation")
    public AjaxResult operationInformation(@RequestBody StrategyBO strategyBO)
    {
        return success(strategyService.operationInformation(strategyBO));
    }
    /**
     * 回测
     */
    @ApiOperation(value = "回测")
    @PreAuthorize("@ss.hasPermi('system:strategy:backtesting')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/backTesting")
    public AjaxResult backTesting(@RequestBody BackTestingBO backTestingBO)
    {
        return success(strategyService.backTesting(backTestingBO));
    }
    /**
     * 查询正在运行的策略
     */
    @ApiOperation(value = "查询正在运行的策略")
    @PreAuthorize("@ss.hasPermi('system:strategy:runningstrategies')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/runningStrategies")
    public AjaxResult runningStrategies(@RequestBody StrategyBO StrategyBO)
    {

        return success(strategyService.runningStrategies(StrategyBO));
    }
    @ApiOperation(value = "查询订单列表")
    @PreAuthorize("@ss.hasPermi('system:strategy:orders')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/orders")
    public AjaxResult getOrders(@RequestBody StrategyBO StrategyBO)
    {
        return success(strategyService.getOrders(StrategyBO));
    }

    @ApiOperation(value = "查询持仓列表")
    @PreAuthorize("@ss.hasPermi('system:strategy:positions')")
    @Log(title = "策略", businessType = BusinessType.OTHER)
    @PostMapping("/positions")
    public AjaxResult getPositions(@RequestBody StrategyBO StrategyBO)
    {
        return success(strategyService.getPositions(StrategyBO));
    }


}
