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
import com.ruoyi.dk.quant.domain.UserStrategyPosition;
import com.ruoyi.dk.quant.service.IUserStrategyPositionService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 策略仓位Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "策略仓位相关接口")
@RestController
@RequestMapping("/system/position")
public class UserStrategyPositionController extends BaseController
{
    @Autowired
    private IUserStrategyPositionService userStrategyPositionService;

    /**
     * 查询策略仓位列表
     */
    @ApiOperation(value = "查询策略仓位列表")
    @PreAuthorize("@ss.hasPermi('system:position:list')")
    @GetMapping("/list")
    public TableDataInfo list(UserStrategyPosition userStrategyPosition)
    {
        startPage();
        List<UserStrategyPosition> list = userStrategyPositionService.selectUserStrategyPositionList(userStrategyPosition);
        return getDataTable(list);
    }

    /**
     * 导出策略仓位列表
     */
    @ApiOperation(value = "导出策略仓位列表")
    @PreAuthorize("@ss.hasPermi('system:position:export')")
    @Log(title = "策略仓位", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, UserStrategyPosition userStrategyPosition)
    {
        List<UserStrategyPosition> list = userStrategyPositionService.selectUserStrategyPositionList(userStrategyPosition);
        ExcelUtil<UserStrategyPosition> util = new ExcelUtil<UserStrategyPosition>(UserStrategyPosition.class);
        util.exportExcel(response, list, "策略仓位数据");
    }

    /**
     * 获取策略仓位详细信息
     */
    @ApiOperation(value = "获取策略仓位详细信息")
    @PreAuthorize("@ss.hasPermi('system:position:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(userStrategyPositionService.selectUserStrategyPositionById(id));
    }

    /**
     * 新增策略仓位
     */
    @ApiOperation(value = "新增策略仓位")
    @PreAuthorize("@ss.hasPermi('system:position:add')")
    @Log(title = "策略仓位", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody UserStrategyPosition userStrategyPosition)
    {
        return toAjax(userStrategyPositionService.insertUserStrategyPosition(userStrategyPosition));
    }

    /**
     * 修改策略仓位
     */
    @ApiOperation(value = "修改策略仓位")
    @PreAuthorize("@ss.hasPermi('system:position:edit')")
    @Log(title = "策略仓位", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody UserStrategyPosition userStrategyPosition)
    {
        return toAjax(userStrategyPositionService.updateUserStrategyPosition(userStrategyPosition));
    }

    /**
     * 删除策略仓位
     */
    @ApiOperation(value = "删除策略仓位")
    @PreAuthorize("@ss.hasPermi('system:position:remove')")
    @Log(title = "策略仓位", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(userStrategyPositionService.deleteUserStrategyPositionByIds(ids));
    }
}
