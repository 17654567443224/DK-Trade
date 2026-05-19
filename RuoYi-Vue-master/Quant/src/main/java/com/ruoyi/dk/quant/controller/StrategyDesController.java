package com.ruoyi.dk.quant.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;
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
import com.ruoyi.dk.quant.domain.StrategyDes;
import com.ruoyi.dk.quant.service.IStrategyDesService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 策略描述Controller
 * 
 * @author ruoyi
 * @date 2025-03-31
 */
@RestController
@RequestMapping("/system/des")
public class StrategyDesController extends BaseController
{
    @Autowired
    private IStrategyDesService strategyDesService;

    /**
     * 查询策略描述列表
     */
    @PreAuthorize("@ss.hasPermi('system:des:list')")
    @GetMapping("/list")
    public TableDataInfo list(StrategyDes strategyDes)
    {
        startPage();
        List<StrategyDes> list = strategyDesService.selectStrategyDesList(strategyDes);
        return getDataTable(list);
    }

    /**
     * 导出策略描述列表
     */
    @PreAuthorize("@ss.hasPermi('system:des:export')")
    @Log(title = "策略描述", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, StrategyDes strategyDes)
    {
        List<StrategyDes> list = strategyDesService.selectStrategyDesList(strategyDes);
        ExcelUtil<StrategyDes> util = new ExcelUtil<StrategyDes>(StrategyDes.class);
        util.exportExcel(response, list, "策略描述数据");
    }

    /**
     * 获取策略描述详细信息
     */
    @PreAuthorize("@ss.hasPermi('system:des:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(strategyDesService.selectStrategyDesById(id));
    }

    /**
     * 新增策略描述
     */
    @PreAuthorize("@ss.hasPermi('system:des:add')")
    @Log(title = "策略描述", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StrategyDes strategyDes)
    {
        return toAjax(strategyDesService.insertStrategyDes(strategyDes));
    }

    /**
     * 修改策略描述
     */
    @PreAuthorize("@ss.hasPermi('system:des:edit')")
    @Log(title = "策略描述", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StrategyDes strategyDes)
    {
        return toAjax(strategyDesService.updateStrategyDes(strategyDes));
    }

    /**
     * 删除策略描述
     */
    @PreAuthorize("@ss.hasPermi('system:des:remove')")
    @Log(title = "策略描述", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(strategyDesService.deleteStrategyDesByIds(ids));
    }
}
