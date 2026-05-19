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
import com.ruoyi.dk.quant.domain.UserStrategyAccount;
import com.ruoyi.dk.quant.service.IUserStrategyAccountService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 策略账户信息Controller
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Api(tags = "策略账户信息相关接口")
@RestController
@RequestMapping("/system/account")
public class UserStrategyAccountController extends BaseController
{
    @Autowired
    private IUserStrategyAccountService userStrategyAccountService;

    /**
     * 查询策略账户信息列表
     */
    @ApiOperation(value = "查询策略账户信息列表")
    @PreAuthorize("@ss.hasPermi('system:account:list')")
    @GetMapping("/list")
    public TableDataInfo list(UserStrategyAccount userStrategyAccount)
    {
        startPage();
        List<UserStrategyAccount> list = userStrategyAccountService.selectUserStrategyAccountList(userStrategyAccount);
        return getDataTable(list);
    }

    /**
     * 导出策略账户信息列表
     */
    @ApiOperation(value = "导出策略账户信息列表")
    @PreAuthorize("@ss.hasPermi('system:account:export')")
    @Log(title = "策略账户信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, UserStrategyAccount userStrategyAccount)
    {
        List<UserStrategyAccount> list = userStrategyAccountService.selectUserStrategyAccountList(userStrategyAccount);
        ExcelUtil<UserStrategyAccount> util = new ExcelUtil<UserStrategyAccount>(UserStrategyAccount.class);
        util.exportExcel(response, list, "策略账户信息数据");
    }

    /**
     * 获取策略账户信息详细信息
     */
    @ApiOperation(value = "获取策略账户信息详细信息")
    @PreAuthorize("@ss.hasPermi('system:account:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(userStrategyAccountService.selectUserStrategyAccountById(id));
    }

    /**
     * 新增策略账户信息
     */
    @ApiOperation(value = "新增策略账户信息")
    @PreAuthorize("@ss.hasPermi('system:account:add')")
    @Log(title = "策略账户信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody UserStrategyAccount userStrategyAccount)
    {
        userStrategyAccountService.insertUserStrategyAccount(userStrategyAccount);
        return success(userStrategyAccount.getId());
    }

    /**
     * 修改策略账户信息
     */
    @ApiOperation(value = "修改策略账户信息")
    @PreAuthorize("@ss.hasPermi('system:account:edit')")
    @Log(title = "策略账户信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody UserStrategyAccount userStrategyAccount)
    {
        return toAjax(userStrategyAccountService.updateUserStrategyAccount(userStrategyAccount));
    }

    /**
     * 删除策略账户信息
     */
    @ApiOperation(value = "删除策略账户信息")
    @PreAuthorize("@ss.hasPermi('system:account:remove')")
    @Log(title = "策略账户信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(userStrategyAccountService.deleteUserStrategyAccountByIds(ids));
    }
}
