package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.UserStrategyAccount;

/**
 * 策略账户信息Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface UserStrategyAccountMapper 
{
    /**
     * 查询策略账户信息
     * 
     * @param id 策略账户信息主键
     * @return 策略账户信息
     */
    public UserStrategyAccount selectUserStrategyAccountById(Long id);

    /**
     * 查询策略账户信息列表
     * 
     * @param userStrategyAccount 策略账户信息
     * @return 策略账户信息集合
     */
    public List<UserStrategyAccount> selectUserStrategyAccountList(UserStrategyAccount userStrategyAccount);

    /**
     * 新增策略账户信息
     * 
     * @param userStrategyAccount 策略账户信息
     * @return 结果
     */
    public int insertUserStrategyAccount(UserStrategyAccount userStrategyAccount);

    /**
     * 修改策略账户信息
     * 
     * @param userStrategyAccount 策略账户信息
     * @return 结果
     */
    public int updateUserStrategyAccount(UserStrategyAccount userStrategyAccount);

    /**
     * 删除策略账户信息
     * 
     * @param id 策略账户信息主键
     * @return 结果
     */
    public int deleteUserStrategyAccountById(Long id);

    /**
     * 批量删除策略账户信息
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteUserStrategyAccountByIds(Long[] ids);
}
