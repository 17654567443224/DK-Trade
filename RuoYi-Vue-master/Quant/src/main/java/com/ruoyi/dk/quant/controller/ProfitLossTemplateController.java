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
import com.ruoyi.dk.quant.domain.ProfitLossTemplate;
import com.ruoyi.dk.quant.service.IProfitLossTemplateService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 止盈止损策略模板Controller
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@RestController
@RequestMapping("/template/profit_loss_template")
public class ProfitLossTemplateController extends BaseController
{
    @Autowired
    private IProfitLossTemplateService profitLossTemplateService;

    /**
     * 查询止盈止损策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:profit_loss_template:list')")
    @GetMapping("/list")
    public TableDataInfo list(ProfitLossTemplate profitLossTemplate)
    {
        startPage();
        List<ProfitLossTemplate> list = profitLossTemplateService.selectProfitLossTemplateList(profitLossTemplate);
        return getDataTable(list);
    }

    /**
     * 导出止盈止损策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:profit_loss_template:export')")
    @Log(title = "止盈止损策略模板", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, ProfitLossTemplate profitLossTemplate)
    {
        List<ProfitLossTemplate> list = profitLossTemplateService.selectProfitLossTemplateList(profitLossTemplate);
        ExcelUtil<ProfitLossTemplate> util = new ExcelUtil<ProfitLossTemplate>(ProfitLossTemplate.class);
        util.exportExcel(response, list, "止盈止损策略模板数据");
    }

    /**
     * 获取止盈止损策略模板详细信息
     */
    @PreAuthorize("@ss.hasPermi('template:profit_loss_template:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(profitLossTemplateService.selectProfitLossTemplateById(id));
    }

    /**
     * 新增止盈止损策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:profit_loss_template:add')")
    @Log(title = "止盈止损策略模板", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody ProfitLossTemplate profitLossTemplate)
    {
        return toAjax(profitLossTemplateService.insertProfitLossTemplate(profitLossTemplate));
    }

    /**
     * 修改止盈止损策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:profit_loss_template:edit')")
    @Log(title = "止盈止损策略模板", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody ProfitLossTemplate profitLossTemplate)
    {
        return toAjax(profitLossTemplateService.updateProfitLossTemplate(profitLossTemplate));
    }

    /**
     * 删除止盈止损策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:profit_loss_template:remove')")
    @Log(title = "止盈止损策略模板", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(profitLossTemplateService.deleteProfitLossTemplateByIds(ids));
    }
}
