package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.UserStrategyPosition;

/**
 * 策略仓位Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface UserStrategyPositionMapper 
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
     * 删除策略仓位
     * 
     * @param id 策略仓位主键
     * @return 结果
     */
    public int deleteUserStrategyPositionById(Long id);

    /**
     * 批量删除策略仓位
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteUserStrategyPositionByIds(Long[] ids);
}
