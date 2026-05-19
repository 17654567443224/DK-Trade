package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.StrategySymbolSelection;

/**
 * 选股策略Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface StrategySymbolSelectionMapper 
{
    /**
     * 查询选股策略
     * 
     * @param id 选股策略主键
     * @return 选股策略
     */
    public StrategySymbolSelection selectStrategySymbolSelectionById(Long id);

    /**
     * 查询选股策略列表
     * 
     * @param strategySymbolSelection 选股策略
     * @return 选股策略集合
     */
    public List<StrategySymbolSelection> selectStrategySymbolSelectionList(StrategySymbolSelection strategySymbolSelection);

    /**
     * 新增选股策略
     * 
     * @param strategySymbolSelection 选股策略
     * @return 结果
     */
    public int insertStrategySymbolSelection(StrategySymbolSelection strategySymbolSelection);

    /**
     * 修改选股策略
     * 
     * @param strategySymbolSelection 选股策略
     * @return 结果
     */
    public int updateStrategySymbolSelection(StrategySymbolSelection strategySymbolSelection);

    /**
     * 删除选股策略
     * 
     * @param id 选股策略主键
     * @return 结果
     */
    public int deleteStrategySymbolSelectionById(Long id);

    /**
     * 批量删除选股策略
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategySymbolSelectionByIds(Long[] ids);
}
