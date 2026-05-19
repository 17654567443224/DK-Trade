package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.SymbolSelectionTemplate;

/**
 * 选股策略模板Mapper接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface SymbolSelectionTemplateMapper 
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
     * 删除选股策略模板
     * 
     * @param id 选股策略模板主键
     * @return 结果
     */
    public int deleteSymbolSelectionTemplateById(Long id);

    /**
     * 批量删除选股策略模板
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteSymbolSelectionTemplateByIds(Long[] ids);
}
