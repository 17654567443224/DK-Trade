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
import com.ruoyi.dk.quant.domain.SymbolSelectionTemplate;
import com.ruoyi.dk.quant.service.ISymbolSelectionTemplateService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 选股策略模板Controller
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@RestController
@RequestMapping("/template/symbol_selection_template")
public class SymbolSelectionTemplateController extends BaseController
{
    @Autowired
    private ISymbolSelectionTemplateService symbolSelectionTemplateService;

    /**
     * 查询选股策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:symbol_selection_template:list')")
    @GetMapping("/list")
    public TableDataInfo list(SymbolSelectionTemplate symbolSelectionTemplate)
    {
        startPage();
        List<SymbolSelectionTemplate> list = symbolSelectionTemplateService.selectSymbolSelectionTemplateList(symbolSelectionTemplate);
        return getDataTable(list);
    }

    /**
     * 导出选股策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:symbol_selection_template:export')")
    @Log(title = "选股策略模板", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, SymbolSelectionTemplate symbolSelectionTemplate)
    {
        List<SymbolSelectionTemplate> list = symbolSelectionTemplateService.selectSymbolSelectionTemplateList(symbolSelectionTemplate);
        ExcelUtil<SymbolSelectionTemplate> util = new ExcelUtil<SymbolSelectionTemplate>(SymbolSelectionTemplate.class);
        util.exportExcel(response, list, "选股策略模板数据");
    }

    /**
     * 获取选股策略模板详细信息
     */
    @PreAuthorize("@ss.hasPermi('template:symbol_selection_template:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(symbolSelectionTemplateService.selectSymbolSelectionTemplateById(id));
    }

    /**
     * 新增选股策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:symbol_selection_template:add')")
    @Log(title = "选股策略模板", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody SymbolSelectionTemplate symbolSelectionTemplate)
    {
        return toAjax(symbolSelectionTemplateService.insertSymbolSelectionTemplate(symbolSelectionTemplate));
    }

    /**
     * 修改选股策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:symbol_selection_template:edit')")
    @Log(title = "选股策略模板", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody SymbolSelectionTemplate symbolSelectionTemplate)
    {
        return toAjax(symbolSelectionTemplateService.updateSymbolSelectionTemplate(symbolSelectionTemplate));
    }

    /**
     * 删除选股策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:symbol_selection_template:remove')")
    @Log(title = "选股策略模板", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(symbolSelectionTemplateService.deleteSymbolSelectionTemplateByIds(ids));
    }
}
