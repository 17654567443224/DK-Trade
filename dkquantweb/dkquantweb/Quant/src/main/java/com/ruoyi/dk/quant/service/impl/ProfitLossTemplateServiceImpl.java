package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.ProfitLossTemplateMapper;
import com.ruoyi.dk.quant.domain.ProfitLossTemplate;
import com.ruoyi.dk.quant.service.IProfitLossTemplateService;

/**
 * 止盈止损策略模板Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@Service
public class ProfitLossTemplateServiceImpl implements IProfitLossTemplateService 
{
    @Autowired
    private ProfitLossTemplateMapper profitLossTemplateMapper;

    /**
     * 查询止盈止损策略模板
     * 
     * @param id 止盈止损策略模板主键
     * @return 止盈止损策略模板
     */
    @Override
    public ProfitLossTemplate selectProfitLossTemplateById(Long id)
    {
        return profitLossTemplateMapper.selectProfitLossTemplateById(id);
    }

    /**
     * 查询止盈止损策略模板列表
     * 
     * @param profitLossTemplate 止盈止损策略模板
     * @return 止盈止损策略模板
     */
    @Override
    public List<ProfitLossTemplate> selectProfitLossTemplateList(ProfitLossTemplate profitLossTemplate)
    {
        return profitLossTemplateMapper.selectProfitLossTemplateList(profitLossTemplate);
    }

    /**
     * 新增止盈止损策略模板
     * 
     * @param profitLossTemplate 止盈止损策略模板
     * @return 结果
     */
    @Override
    public int insertProfitLossTemplate(ProfitLossTemplate profitLossTemplate)
    {
        return profitLossTemplateMapper.insertProfitLossTemplate(profitLossTemplate);
    }

    /**
     * 修改止盈止损策略模板
     * 
     * @param profitLossTemplate 止盈止损策略模板
     * @return 结果
     */
    @Override
    public int updateProfitLossTemplate(ProfitLossTemplate profitLossTemplate)
    {
        return profitLossTemplateMapper.updateProfitLossTemplate(profitLossTemplate);
    }

    /**
     * 批量删除止盈止损策略模板
     * 
     * @param ids 需要删除的止盈止损策略模板主键
     * @return 结果
     */
    @Override
    public int deleteProfitLossTemplateByIds(Long[] ids)
    {
        return profitLossTemplateMapper.deleteProfitLossTemplateByIds(ids);
    }

    /**
     * 删除止盈止损策略模板信息
     * 
     * @param id 止盈止损策略模板主键
     * @return 结果
     */
    @Override
    public int deleteProfitLossTemplateById(Long id)
    {
        return profitLossTemplateMapper.deleteProfitLossTemplateById(id);
    }
}
