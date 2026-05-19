package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.SymbolSelectionTemplate;

/**
 * 选股策略模板Service接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface ISymbolSelectionTemplateService 
{
    /**
     * 查询选股策略模板
     * 
     * @param id 选股策略模板主键
     * @return 选股策略模板
     */
    public SymbolSelectionTemplate selectSymbolSelectionTemplateById(Long id);

    /**
     * 查询选股策略模板列表
     * 
     * @param symbolSelectionTemplate 选股策略模板
     * @return 选股策略模板集合
     */
    public List<SymbolSelectionTemplate> selectSymbolSelectionTemplateList(SymbolSelectionTemplate symbolSelectionTemplate);

    /**
     * 新增选股策略模板
     * 
     * @param symbolSelectionTemplate 选股策略模板
     * @return 结果
     */
    public int insertSymbolSelectionTemplate(SymbolSelectionTemplate symbolSelectionTemplate);

    /**
     * 修改选股策略模板
     * 
     * @param symbolSelectionTemplate 选股策略模板
     * @return 结果
     */
    public int updateSymbolSelectionTemplate(SymbolSelectionTemplate symbolSelectionTemplate);

    /**
     * 批量删除选股策略模板
     * 
     * @param ids 需要删除的选股策略模板主键集合
     * @return 结果
     */
    public int deleteSymbolSelectionTemplateByIds(Long[] ids);

    /**
     * 删除选股策略模板信息
     * 
     * @param id 选股策略模板主键
     * @return 结果
     */
    public int deleteSymbolSelectionTemplateById(Long id);
}
