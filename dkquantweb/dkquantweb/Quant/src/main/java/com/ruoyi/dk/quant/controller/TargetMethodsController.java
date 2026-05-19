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
import com.ruoyi.dk.quant.domain.TargetMethods;
import com.ruoyi.dk.quant.service.ITargetMethodsService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 指标Controller
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@RestController
@RequestMapping("/template/target")
public class TargetMethodsController extends BaseController
{
    @Autowired
    private ITargetMethodsService targetMethodsService;

    /**
     * 查询指标列表
     */
    @PreAuthorize("@ss.hasPermi('template:target:list')")
    @GetMapping("/list")
    public TableDataInfo list(TargetMethods targetMethods)
    {
        startPage();
        List<TargetMethods> list = targetMethodsService.selectTargetMethodsList(targetMethods);
        return getDataTable(list);
    }

    /**
     * 导出指标列表
     */
    @PreAuthorize("@ss.hasPermi('template:target:export')")
    @Log(title = "指标", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, TargetMethods targetMethods)
    {
        List<TargetMethods> list = targetMethodsService.selectTargetMethodsList(targetMethods);
        ExcelUtil<TargetMethods> util = new ExcelUtil<TargetMethods>(TargetMethods.class);
        util.exportExcel(response, list, "指标数据");
    }

    /**
     * 获取指标详细信息
     */
    @PreAuthorize("@ss.hasPermi('template:target:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(targetMethodsService.selectTargetMethodsById(id));
    }

    /**
     * 新增指标
     */
    @PreAuthorize("@ss.hasPermi('template:target:add')")
    @Log(title = "指标", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody TargetMethods targetMethods)
    {
        return toAjax(targetMethodsService.insertTargetMethods(targetMethods));
    }

    /**
     * 修改指标
     */
    @PreAuthorize("@ss.hasPermi('template:target:edit')")
    @Log(title = "指标", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody TargetMethods targetMethods)
    {
        return toAjax(targetMethodsService.updateTargetMethods(targetMethods));
    }

    /**
     * 删除指标
     */
    @PreAuthorize("@ss.hasPermi('template:target:remove')")
    @Log(title = "指标", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(targetMethodsService.deleteTargetMethodsByIds(ids));
    }
}
