package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.UserStrategyAccountMapper;
import com.ruoyi.dk.quant.domain.UserStrategyAccount;
import com.ruoyi.dk.quant.service.IUserStrategyAccountService;

/**
 * 策略账户信息Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class UserStrategyAccountServiceImpl implements IUserStrategyAccountService 
{
    @Autowired
    private UserStrategyAccountMapper userStrategyAccountMapper;

    /**
     * 查询策略账户信息
     * 
     * @param id 策略账户信息主键
     * @return 策略账户信息
     */
    @Override
    public UserStrategyAccount selectUserStrategyAccountById(Long id)
    {
        return userStrategyAccountMapper.selectUserStrategyAccountById(id);
    }

    /**
     * 查询策略账户信息列表
     * 
     * @param userStrategyAccount 策略账户信息
     * @return 策略账户信息
     */
    @Override
    public List<UserStrategyAccount> selectUserStrategyAccountList(UserStrategyAccount userStrategyAccount)
    {
        return userStrategyAccountMapper.selectUserStrategyAccountList(userStrategyAccount);
    }

    /**
     * 新增策略账户信息
     * 
     * @param userStrategyAccount 策略账户信息
     * @return 结果
     */
    @Override
    public int insertUserStrategyAccount(UserStrategyAccount userStrategyAccount)
    {
        return userStrategyAccountMapper.insertUserStrategyAccount(userStrategyAccount);
    }

    /**
     * 修改策略账户信息
     * 
     * @param userStrategyAccount 策略账户信息
     * @return 结果
     */
    @Override
    public int updateUserStrategyAccount(UserStrategyAccount userStrategyAccount)
    {
        return userStrategyAccountMapper.updateUserStrategyAccount(userStrategyAccount);
    }

    /**
     * 批量删除策略账户信息
     * 
     * @param ids 需要删除的策略账户信息主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyAccountByIds(Long[] ids)
    {
        return userStrategyAccountMapper.deleteUserStrategyAccountByIds(ids);
    }

    /**
     * 删除策略账户信息信息
     * 
     * @param id 策略账户信息主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyAccountById(Long id)
    {
        return userStrategyAccountMapper.deleteUserStrategyAccountById(id);
    }
}
