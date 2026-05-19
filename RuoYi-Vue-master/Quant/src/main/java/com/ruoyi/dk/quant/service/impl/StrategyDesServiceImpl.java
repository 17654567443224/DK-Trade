package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategyDesMapper;
import com.ruoyi.dk.quant.domain.StrategyDes;
import com.ruoyi.dk.quant.service.IStrategyDesService;

/**
 * 策略描述Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-03-31
 */
@Service
public class StrategyDesServiceImpl implements IStrategyDesService 
{
    @Autowired
    private StrategyDesMapper strategyDesMapper;

    /**
     * 查询策略描述
     * 
     * @param id 策略描述主键
     * @return 策略描述
     */
    @Override
    public StrategyDes selectStrategyDesById(Long id)
    {
        return strategyDesMapper.selectStrategyDesById(id);
    }

    /**
     * 查询策略描述列表
     * 
     * @param strategyDes 策略描述
     * @return 策略描述
     */
    @Override
    public List<StrategyDes> selectStrategyDesList(StrategyDes strategyDes)
    {
        return strategyDesMapper.selectStrategyDesList(strategyDes);
    }

    /**
     * 新增策略描述
     * 
     * @param strategyDes 策略描述
     * @return 结果
     */
    @Override
    public int insertStrategyDes(StrategyDes strategyDes)
    {
        return strategyDesMapper.insertStrategyDes(strategyDes);
    }

    /**
     * 修改策略描述
     * 
     * @param strategyDes 策略描述
     * @return 结果
     */
    @Override
    public int updateStrategyDes(StrategyDes strategyDes)
    {
        return strategyDesMapper.updateStrategyDes(strategyDes);
    }

    /**
     * 批量删除策略描述
     * 
     * @param ids 需要删除的策略描述主键
     * @return 结果
     */
    @Override
    public int deleteStrategyDesByIds(Long[] ids)
    {
        return strategyDesMapper.deleteStrategyDesByIds(ids);
    }

    /**
     * 删除策略描述信息
     * 
     * @param id 策略描述主键
     * @return 结果
     */
    @Override
    public int deleteStrategyDesById(Long id)
    {
        return strategyDesMapper.deleteStrategyDesById(id);
    }
}
