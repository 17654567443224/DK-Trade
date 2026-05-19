package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategyPvMapper;
import com.ruoyi.dk.quant.domain.StrategyPv;
import com.ruoyi.dk.quant.service.IStrategyPvService;

/**
 * 私有策略Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class StrategyPvServiceImpl implements IStrategyPvService 
{
    @Autowired
    private StrategyPvMapper strategyPvMapper;

    /**
     * 查询私有策略
     * 
     * @param id 私有策略主键
     * @return 私有策略
     */
    @Override
    public StrategyPv selectStrategyPvById(Long id)
    {
        return strategyPvMapper.selectStrategyPvById(id);
    }

    /**
     * 查询私有策略列表
     * 
     * @param strategyPv 私有策略
     * @return 私有策略
     */
    @Override
    public List<StrategyPv> selectStrategyPvList(StrategyPv strategyPv)
    {
        return strategyPvMapper.selectStrategyPvList(strategyPv);
    }

    /**
     * 新增私有策略
     * 
     * @param strategyPv 私有策略
     * @return 结果
     */
    @Override
    public int insertStrategyPv(StrategyPv strategyPv)
    {
        return strategyPvMapper.insertStrategyPv(strategyPv);
    }

    /**
     * 修改私有策略
     * 
     * @param strategyPv 私有策略
     * @return 结果
     */
    @Override
    public int updateStrategyPv(StrategyPv strategyPv)
    {
        return strategyPvMapper.updateStrategyPv(strategyPv);
    }

    /**
     * 批量删除私有策略
     * 
     * @param ids 需要删除的私有策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyPvByIds(Long[] ids)
    {
        return strategyPvMapper.deleteStrategyPvByIds(ids);
    }

    /**
     * 删除私有策略信息
     * 
     * @param id 私有策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyPvById(Long id)
    {
        return strategyPvMapper.deleteStrategyPvById(id);
    }
}
