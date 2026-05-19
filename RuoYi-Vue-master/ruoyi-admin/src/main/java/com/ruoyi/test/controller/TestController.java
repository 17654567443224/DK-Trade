package com.ruoyi.test.controller;

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
import com.ruoyi.test.domain.Test;
import com.ruoyi.test.service.ITestService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 测试用Controller
 * 
 * @author ruoyi
 * @date 2025-02-01
 */
@RestController
@RequestMapping("/test/test")
public class TestController extends BaseController
{
    @Autowired
    private ITestService testService;

    /**
     * 查询测试用列表
     */
    @PreAuthorize("@ss.hasPermi('test:test:list')")
    @GetMapping("/list")
    public TableDataInfo list(Test test)
    {
        startPage();
        List<Test> list = testService.selectTestList(test);
        return getDataTable(list);
    }

    /**
     * 导出测试用列表
     */
    @PreAuthorize("@ss.hasPermi('test:test:export')")
    @Log(title = "测试用", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Test test)
    {
        List<Test> list = testService.selectTestList(test);
        ExcelUtil<Test> util = new ExcelUtil<Test>(Test.class);
        util.exportExcel(response, list, "测试用数据");
    }

    /**
     * 获取测试用详细信息
     */
    @PreAuthorize("@ss.hasPermi('test:test:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(testService.selectTestById(id));
    }

    /**
     * 新增测试用
     */
    @PreAuthorize("@ss.hasPermi('test:test:add')")
    @Log(title = "测试用", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Test test)
    {
        return toAjax(testService.insertTest(test));
    }

    /**
     * 修改测试用
     */
    @PreAuthorize("@ss.hasPermi('test:test:edit')")
    @Log(title = "测试用", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Test test)
    {
        return toAjax(testService.updateTest(test));
    }

    /**
     * 删除测试用
     */
    @PreAuthorize("@ss.hasPermi('test:test:remove')")
    @Log(title = "测试用", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(testService.deleteTestByIds(ids));
    }
}
