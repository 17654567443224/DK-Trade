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
import com.ruoyi.dk.quant.domain.OpenPositionTemplate;
import com.ruoyi.dk.quant.service.IOpenPositionTemplateService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 开仓策略模板Controller
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@RestController
@RequestMapping("/template/open_position_template")
public class OpenPositionTemplateController extends BaseController
{
    @Autowired
    private IOpenPositionTemplateService openPositionTemplateService;

    /**
     * 查询开仓策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:open_position_template:list')")
    @GetMapping("/list")
    public TableDataInfo list(OpenPositionTemplate openPositionTemplate)
    {
        startPage();
        List<OpenPositionTemplate> list = openPositionTemplateService.selectOpenPositionTemplateList(openPositionTemplate);
        return getDataTable(list);
    }

    /**
     * 导出开仓策略模板列表
     */
    @PreAuthorize("@ss.hasPermi('template:open_position_template:export')")
    @Log(title = "开仓策略模板", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, OpenPositionTemplate openPositionTemplate)
    {
        List<OpenPositionTemplate> list = openPositionTemplateService.selectOpenPositionTemplateList(openPositionTemplate);
        ExcelUtil<OpenPositionTemplate> util = new ExcelUtil<OpenPositionTemplate>(OpenPositionTemplate.class);
        util.exportExcel(response, list, "开仓策略模板数据");
    }

    /**
     * 获取开仓策略模板详细信息
     */
    @PreAuthorize("@ss.hasPermi('template:open_position_template:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(openPositionTemplateService.selectOpenPositionTemplateById(id));
    }

    /**
     * 新增开仓策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:open_position_template:add')")
    @Log(title = "开仓策略模板", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody OpenPositionTemplate openPositionTemplate)
    {
        return toAjax(openPositionTemplateService.insertOpenPositionTemplate(openPositionTemplate));
    }

    /**
     * 修改开仓策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:open_position_template:edit')")
    @Log(title = "开仓策略模板", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody OpenPositionTemplate openPositionTemplate)
    {
        return toAjax(openPositionTemplateService.updateOpenPositionTemplate(openPositionTemplate));
    }

    /**
     * 删除开仓策略模板
     */
    @PreAuthorize("@ss.hasPermi('template:open_position_template:remove')")
    @Log(title = "开仓策略模板", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(openPositionTemplateService.deleteOpenPositionTemplateByIds(ids));
    }
}
