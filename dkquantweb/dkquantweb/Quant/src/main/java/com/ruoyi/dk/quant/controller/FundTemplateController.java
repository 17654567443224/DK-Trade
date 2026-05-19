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
import com.ruoyi.dk.quant.domain.FundTemplate;
import com.ruoyi.dk.quant.service.IFundTemplateService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 资金策略模板Controller
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@RestController
@RequestMapping("/template/fund_template")
public class FundTemplateController extends BaseController
{
    @Autowired
    private IFundTemplateService fundTemplateService;

    /**
     * 查询资金策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:fund_template:list')")
    @GetMapping("/list")
    public TableDataInfo list(FundTemplate fundTemplate)
    {
        startPage();
        List<FundTemplate> list = fundTemplateService.selectFundTemplateList(fundTemplate);
        return getDataTable(list);
    }

    /**
     * 导出资金策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:fund_template:export')")
    @Log(title = "资金策略模板", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, FundTemplate fundTemplate)
    {
        List<FundTemplate> list = fundTemplateService.selectFundTemplateList(fundTemplate);
        ExcelUtil<FundTemplate> util = new ExcelUtil<FundTemplate>(FundTemplate.class);
        util.exportExcel(response, list, "资金策略模板数据");
    }

    /**
     * 获取资金策略模板详细信息
     */
    @PreAuthorize("@ss.hasPermi('template:fund_template:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(fundTemplateService.selectFundTemplateById(id));
    }

    /**
     * 新增资金策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:fund_template:add')")
    @Log(title = "资金策略模板", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody FundTemplate fundTemplate)
    {
        return toAjax(fundTemplateService.insertFundTemplate(fundTemplate));
    }

    /**
     * 修改资金策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:fund_template:edit')")
    @Log(title = "资金策略模板", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody FundTemplate fundTemplate)
    {
        return toAjax(fundTemplateService.updateFundTemplate(fundTemplate));
    }

    /**
     * 删除资金策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:fund_template:remove')")
    @Log(title = "资金策略模板", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(fundTemplateService.deleteFundTemplateByIds(ids));
    }
}
