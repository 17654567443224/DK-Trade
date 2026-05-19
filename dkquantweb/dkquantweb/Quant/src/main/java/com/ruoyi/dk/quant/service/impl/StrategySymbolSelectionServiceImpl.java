package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategySymbolSelectionMapper;
import com.ruoyi.dk.quant.domain.StrategySymbolSelection;
import com.ruoyi.dk.quant.service.IStrategySymbolSelectionService;

/**
 * 选股策略Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class StrategySymbolSelectionServiceImpl implements IStrategySymbolSelectionService 
{
    @Autowired
    private StrategySymbolSelectionMapper strategySymbolSelectionMapper;

    /**
     * 查询选股策略
     * 
     * @param id 选股策略主键
     * @return 选股策略
     */
    @Override
    public StrategySymbolSelection selectStrategySymbolSelectionById(Long id)
    {
        return strategySymbolSelectionMapper.selectStrategySymbolSelectionById(id);
    }

    /**
     * 查询选股策略列表
     * 
     * @param strategySymbolSelection 选股策略
     * @return 选股策略
     */
    @Override
    public List<StrategySymbolSelection> selectStrategySymbolSelectionList(StrategySymbolSelection strategySymbolSelection)
    {
        return strategySymbolSelectionMapper.selectStrategySymbolSelectionList(strategySymbolSelection);
    }

    /**
     * 新增选股策略
     * 
     * @param strategySymbolSelection 选股策略
     * @return 结果
     */
    @Override
    public int insertStrategySymbolSelection(StrategySymbolSelection strategySymbolSelection)
    {
        return strategySymbolSelectionMapper.insertStrategySymbolSelection(strategySymbolSelection);
    }

    /**
     * 修改选股策略
     * 
     * @param strategySymbolSelection 选股策略
     * @return 结果
     */
    @Override
    public int updateStrategySymbolSelection(StrategySymbolSelection strategySymbolSelection)
    {
        return strategySymbolSelectionMapper.updateStrategySymbolSelection(strategySymbolSelection);
    }

    /**
     * 批量删除选股策略
     * 
     * @param ids 需要删除的选股策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategySymbolSelectionByIds(Long[] ids)
    {
        return strategySymbolSelectionMapper.deleteStrategySymbolSelectionByIds(ids);
    }

    /**
     * 删除选股策略信息
     * 
     * @param id 选股策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategySymbolSelectionById(Long id)
    {
        return strategySymbolSelectionMapper.deleteStrategySymbolSelectionById(id);
    }
}
