package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.ProfitLossTemplate;

/**
 * 止盈止损策略模板Service接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface IProfitLossTemplateService 
{
    /**
     * 查询止盈止损策略模板
     * 
     * @param id 止盈止损策略模板主键
     * @return 止盈止损策略模板
     */
    public ProfitLossTemplate selectProfitLossTemplateById(Long id);

    /**
     * 查询止盈止损策略模板列表
     * 
     * @param profitLossTemplate 止盈止损策略模板
     * @return 止盈止损策略模板集合
     */
    public List<ProfitLossTemplate> selectProfitLossTemplateList(ProfitLossTemplate profitLossTemplate);

    /**
     * 新增止盈止损策略模板
     * 
     * @param profitLossTemplate 止盈止损策略模板
     * @return 结果
     */
    public int insertProfitLossTemplate(ProfitLossTemplate profitLossTemplate);

    /**
     * 修改止盈止损策略模板
     * 
     * @param profitLossTemplate 止盈止损策略模板
     * @return 结果
     */
    public int updateProfitLossTemplate(ProfitLossTemplate profitLossTemplate);

    /**
     * 批量删除止盈止损策略模板
     * 
     * @param ids 需要删除的止盈止损策略模板主键集合
     * @return 结果
     */
    public int deleteProfitLossTemplateByIds(Long[] ids);

    /**
     * 删除止盈止损策略模板信息
     * 
     * @param id 止盈止损策略模板主键
     * @return 结果
     */
    public int deleteProfitLossTemplateById(Long id);
}
