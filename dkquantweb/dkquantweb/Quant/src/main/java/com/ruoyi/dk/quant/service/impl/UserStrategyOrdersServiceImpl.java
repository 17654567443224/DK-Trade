package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.UserStrategyOrdersMapper;
import com.ruoyi.dk.quant.domain.UserStrategyOrders;
import com.ruoyi.dk.quant.service.IUserStrategyOrdersService;

/**
 * 策略订单信息Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class UserStrategyOrdersServiceImpl implements IUserStrategyOrdersService 
{
    @Autowired
    private UserStrategyOrdersMapper userStrategyOrdersMapper;

    /**
     * 查询策略订单信息
     * 
     * @param id 策略订单信息主键
     * @return 策略订单信息
     */
    @Override
    public UserStrategyOrders selectUserStrategyOrdersById(Long id)
    {
        return userStrategyOrdersMapper.selectUserStrategyOrdersById(id);
    }

    /**
     * 查询策略订单信息列表
     * 
     * @param userStrategyOrders 策略订单信息
     * @return 策略订单信息
     */
    @Override
    public List<UserStrategyOrders> selectUserStrategyOrdersList(UserStrategyOrders userStrategyOrders)
    {
        return userStrategyOrdersMapper.selectUserStrategyOrdersList(userStrategyOrders);
    }

    /**
     * 新增策略订单信息
     * 
     * @param userStrategyOrders 策略订单信息
     * @return 结果
     */
    @Override
    public int insertUserStrategyOrders(UserStrategyOrders userStrategyOrders)
    {
        return userStrategyOrdersMapper.insertUserStrategyOrders(userStrategyOrders);
    }

    /**
     * 修改策略订单信息
     * 
     * @param userStrategyOrders 策略订单信息
     * @return 结果
     */
    @Override
    public int updateUserStrategyOrders(UserStrategyOrders userStrategyOrders)
    {
        return userStrategyOrdersMapper.updateUserStrategyOrders(userStrategyOrders);
    }

    /**
     * 批量删除策略订单信息
     * 
     * @param ids 需要删除的策略订单信息主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyOrdersByIds(Long[] ids)
    {
        return userStrategyOrdersMapper.deleteUserStrategyOrdersByIds(ids);
    }

    /**
     * 删除策略订单信息信息
     * 
     * @param id 策略订单信息主键
     * @return 结果
     */
    @Override
    public int deleteUserStrategyOrdersById(Long id)
    {
        return userStrategyOrdersMapper.deleteUserStrategyOrdersById(id);
    }
}
