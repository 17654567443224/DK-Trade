package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.UserStrategyPositionMapper;
import com.ruoyi.dk.quant.domain.UserStrategyPosition;
import com.ruoyi.dk.quant.service.IUserStrategyPositionService;

/**
 * 策略仓位Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class UserStrategyPositionServiceImpl implements IUserStrategyPositionService 
{
    @Autowired
    private UserStrategyPositionMapper userStrategyPositionMapper;

    /**
     * 查询策略仓位
     * 
     * @param id 策略仓位主键
     * @return 策略仓位
     */
    @Override
    public UserStrategyPosition selectUserStrategyPositionById(Long id)
    {
        return userStrategyPositionMapper.selectUserStrategyPositionById(id);
    }

    /**
     * 查询策略仓位列表
     * 
     * @param userStrategyPosition 策略仓位
     * @return 策略仓位
     */
    @Override
    public List<UserStrategyPosition> selectUserStrategyPositionList(UserStrategyPosition userStrategyPosition)
    {
        return userStrategyPositionMapper.selectUserStrategyPositionList(userStrategyPosition);
    }

    /**
     * 新增策略仓位
     * 
     * @param userStrategyPosition 策略仓位
     * @return 结果
     */
    @Override
    public int insertUserStrategyPosition(UserStrategyPosition userStrategyPosition)
    {
        userStrategyPosition.setCreateTime(DateUtils.getNowDate());
        return userStrategyPositionMapper.insertUserStrategyPosition(userStrategyPosition);
    }

    /**
     * 修改策略仓位
     * 
     * @param userStrategyPosition 策略仓位
     * @return 结果
     */
    @Override
    public int updateUserStrategyPosition(UserStrategyPosition userStrategyPosition)
    {
        return userStrategyPositionMapper.updateUserStrategyPosition(userStrategyPosition);
    }

    /**
     * 批量删除策略仓位
     * 
     * @param ids 需要删除的策略仓位主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyPositionByIds(Long[] ids)
    {
        return userStrategyPositionMapper.deleteUserStrategyPositionByIds(ids);
    }

    /**
     * 删除策略仓位信息
     * 
     * @param id 策略仓位主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyPositionById(Long id)
    {
        return userStrategyPositionMapper.deleteUserStrategyPositionById(id);
    }
}
