package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.ProfitLossTemplate;

/**
 * 止盈止损策略模板Mapper接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface ProfitLossTemplateMapper 
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
     * 删除止盈止损策略模板
     * 
     * @param id 止盈止损策略模板主键
     * @return 结果
     */
    public int deleteProfitLossTemplateById(Long id);

    /**
     * 批量删除止盈止损策略模板
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteProfitLossTemplateByIds(Long[] ids);
}
