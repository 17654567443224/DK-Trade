package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.UserStrategyArgs;

/**
 * 策略参数信息Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-25
 */
public interface UserStrategyArgsMapper 
{
    /**
     * 查询策略参数信息
     * 
     * @param id 策略参数信息主键
     * @return 策略参数信息
     */
    public UserStrategyArgs selectUserStrategyArgsById(Long id);

    /**
     * 查询策略参数信息列表
     * 
     * @param userStrategyArgs 策略参数信息
     * @return 策略参数信息集合
     */
    public List<UserStrategyArgs> selectUserStrategyArgsList(UserStrategyArgs userStrategyArgs);

    /**
     * 新增策略参数信息
     * 
     * @param userStrategyArgs 策略参数信息
     * @return 结果
     */
    public int insertUserStrategyArgs(UserStrategyArgs userStrategyArgs);

    /**
     * 修改策略参数信息
     * 
     * @param userStrategyArgs 策略参数信息
     * @return 结果
     */
    public int updateUserStrategyArgs(UserStrategyArgs userStrategyArgs);

    /**
     * 删除策略参数信息
     * 
     * @param id 策略参数信息主键
     * @return 结果
     */
    public int deleteUserStrategyArgsById(Long id);

    /**
     * 批量删除策略参数信息
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteUserStrategyArgsByIds(Long[] ids);
}
