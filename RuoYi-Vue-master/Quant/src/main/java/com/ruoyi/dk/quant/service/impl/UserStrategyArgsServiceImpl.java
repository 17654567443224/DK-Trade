package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.UserStrategyArgsMapper;
import com.ruoyi.dk.quant.domain.UserStrategyArgs;
import com.ruoyi.dk.quant.service.IUserStrategyArgsService;

/**
 * 策略参数信息Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-25
 */
@Service
public class UserStrategyArgsServiceImpl implements IUserStrategyArgsService 
{
    @Autowired
    private UserStrategyArgsMapper userStrategyArgsMapper;

    /**
     * 查询策略参数信息
     * 
     * @param id 策略参数信息主键
     * @return 策略参数信息
     */
    @Override
    public UserStrategyArgs selectUserStrategyArgsById(Long id)
    {
        return userStrategyArgsMapper.selectUserStrategyArgsById(id);
    }

    /**
     * 查询策略参数信息列表
     * 
     * @param userStrategyArgs 策略参数信息
     * @return 策略参数信息
     */
    @Override
    public List<UserStrategyArgs> selectUserStrategyArgsList(UserStrategyArgs userStrategyArgs)
    {
        return userStrategyArgsMapper.selectUserStrategyArgsList(userStrategyArgs);
    }

    /**
     * 新增策略参数信息
     * 
     * @param userStrategyArgs 策略参数信息
     * @return 结果
     */
    @Override
    public int insertUserStrategyArgs(UserStrategyArgs userStrategyArgs)
    {
        return userStrategyArgsMapper.insertUserStrategyArgs(userStrategyArgs);
    }

    /**
     * 修改策略参数信息
     * 
     * @param userStrategyArgs 策略参数信息
     * @return 结果
     */
    @Override
    public int updateUserStrategyArgs(UserStrategyArgs userStrategyArgs)
    {
        return userStrategyArgsMapper.updateUserStrategyArgs(userStrategyArgs);
    }

    /**
     * 批量删除策略参数信息
     * 
     * @param ids 需要删除的策略参数信息主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyArgsByIds(Long[] ids)
    {
        return userStrategyArgsMapper.deleteUserStrategyArgsByIds(ids);
    }

    /**
     * 删除策略参数信息信息
     * 
     * @param id 策略参数信息主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyArgsById(Long id)
    {
        return userStrategyArgsMapper.deleteUserStrategyArgsById(id);
    }
}
