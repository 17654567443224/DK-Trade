package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategyOpenPositionMapper;
import com.ruoyi.dk.quant.domain.StrategyOpenPosition;
import com.ruoyi.dk.quant.service.IStrategyOpenPositionService;

/**
 * 开仓策略Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class StrategyOpenPositionServiceImpl implements IStrategyOpenPositionService 
{
    @Autowired
    private StrategyOpenPositionMapper strategyOpenPositionMapper;

    /**
     * 查询开仓策略
     * 
     * @param id 开仓策略主键
     * @return 开仓策略
     */
    @Override
    public StrategyOpenPosition selectStrategyOpenPositionById(Long id)
    {
        return strategyOpenPositionMapper.selectStrategyOpenPositionById(id);
    }

    /**
     * 查询开仓策略列表
     * 
     * @param strategyOpenPosition 开仓策略
     * @return 开仓策略
     */
    @Override
    public List<StrategyOpenPosition> selectStrategyOpenPositionList(StrategyOpenPosition strategyOpenPosition)
    {
        return strategyOpenPositionMapper.selectStrategyOpenPositionList(strategyOpenPosition);
    }

    /**
     * 新增开仓策略
     * 
     * @param strategyOpenPosition 开仓策略
     * @return 结果
     */
    @Override
    public int insertStrategyOpenPosition(StrategyOpenPosition strategyOpenPosition)
    {
        return strategyOpenPositionMapper.insertStrategyOpenPosition(strategyOpenPosition);
    }

    /**
     * 修改开仓策略
     * 
     * @param strategyOpenPosition 开仓策略
     * @return 结果
     */
    @Override
    public int updateStrategyOpenPosition(StrategyOpenPosition strategyOpenPosition)
    {
        return strategyOpenPositionMapper.updateStrategyOpenPosition(strategyOpenPosition);
    }

    /**
     * 批量删除开仓策略
     * 
     * @param ids 需要删除的开仓策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyOpenPositionByIds(Long[] ids)
    {
        return strategyOpenPositionMapper.deleteStrategyOpenPositionByIds(ids);
    }

    /**
     * 删除开仓策略信息
     * 
     * @param id 开仓策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyOpenPositionById(Long id)
    {
        return strategyOpenPositionMapper.deleteStrategyOpenPositionById(id);
    }
}
