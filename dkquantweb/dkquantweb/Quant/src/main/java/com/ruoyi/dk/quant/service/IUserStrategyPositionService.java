package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.UserStrategyPosition;

/**
 * 策略仓位Service接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface IUserStrategyPositionService 
{
    /**
     * 查询策略仓位
     * 
     * @param id 策略仓位主键
     * @return 策略仓位
     */
    public UserStrategyPosition selectUserStrategyPositionById(Long id);

    /**
     * 查询策略仓位列表
     * 
     * @param userStrategyPosition 策略仓位
     * @return 策略仓位集合
     */
    public List<UserStrategyPosition> selectUserStrategyPositionList(UserStrategyPosition userStrategyPosition);

    /**
     * 新增策略仓位
     * 
     * @param userStrategyPosition 策略仓位
     * @return 结果
     */
    public int insertUserStrategyPosition(UserStrategyPosition userStrategyPosition);

    /**
     * 修改策略仓位
     * 
     * @param userStrategyPosition 策略仓位
     * @return 结果
     */
    public int updateUserStrategyPosition(UserStrategyPosition userStrategyPosition);

    /**
     * 批量删除策略仓位
     * 
     * @param ids 需要删除的策略仓位主键集合
     * @return 结果
     */
    public int deleteUserStrategyPositionByIds(Long[] ids);

    /**
     * 删除策略仓位信息
     * 
     * @param id 策略仓位主键
     * @return 结果
     */
    public int deleteUserStrategyPositionById(Long id);
}
