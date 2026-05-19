package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.SymbolSelectionTemplateMapper;
import com.ruoyi.dk.quant.domain.SymbolSelectionTemplate;
import com.ruoyi.dk.quant.service.ISymbolSelectionTemplateService;

/**
 * 选股策略模板Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@Service
public class SymbolSelectionTemplateServiceImpl implements ISymbolSelectionTemplateService 
{
    @Autowired
    private SymbolSelectionTemplateMapper symbolSelectionTemplateMapper;

    /**
     * 查询选股策略模板
     * 
     * @param id 选股策略模板主键
     * @return 选股策略模板
     */
    @Override
    public SymbolSelectionTemplate selectSymbolSelectionTemplateById(Long id)
    {
        return symbolSelectionTemplateMapper.selectSymbolSelectionTemplateById(id);
    }

    /**
     * 查询选股策略模板列表
     * 
     * @param symbolSelectionTemplate 选股策略模板
     * @return 选股策略模板
     */
    @Override
    public List<SymbolSelectionTemplate> selectSymbolSelectionTemplateList(SymbolSelectionTemplate symbolSelectionTemplate)
    {
        return symbolSelectionTemplateMapper.selectSymbolSelectionTemplateList(symbolSelectionTemplate);
    }

    /**
     * 新增选股策略模板
     * 
     * @param symbolSelectionTemplate 选股策略模板
     * @return 结果
     */
    @Override
    public int insertSymbolSelectionTemplate(SymbolSelectionTemplate symbolSelectionTemplate)
    {
        return symbolSelectionTemplateMapper.insertSymbolSelectionTemplate(symbolSelectionTemplate);
    }

    /**
     * 修改选股策略模板
     * 
     * @param symbolSelectionTemplate 选股策略模板
     * @return 结果
     */
    @Override
    public int updateSymbolSelectionTemplate(SymbolSelectionTemplate symbolSelectionTemplate)
    {
        return symbolSelectionTemplateMapper.updateSymbolSelectionTemplate(symbolSelectionTemplate);
    }

    /**
     * 批量删除选股策略模板
     * 
     * @param ids 需要删除的选股策略模板主键
     * @return 结果
     */
    @Override
    public int deleteSymbolSelectionTemplateByIds(Long[] ids)
    {
        return symbolSelectionTemplateMapper.deleteSymbolSelectionTemplateByIds(ids);
    }

    /**
     * 删除选股策略模板信息
     * 
     * @param id 选股策略模板主键
     * @return 结果
     */
    @Override
    public int deleteSymbolSelectionTemplateById(Long id)
    {
        return symbolSelectionTemplateMapper.deleteSymbolSelectionTemplateById(id);
    }
}
