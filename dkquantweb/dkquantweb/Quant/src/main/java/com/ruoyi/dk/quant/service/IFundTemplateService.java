package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.FundTemplate;

/**
 * 资金策略模板Service接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface IFundTemplateService 
{
    /**
     * 查询资金策略模板
     * 
     * @param id 资金策略模板主键
     * @return 资金策略模板
     */
    public FundTemplate selectFundTemplateById(Long id);

    /**
     * 查询资金策略模板列表
     * 
     * @param fundTemplate 资金策略模板
     * @return 资金策略模板集合
     */
    public List<FundTemplate> selectFundTemplateList(FundTemplate fundTemplate);

    /**
     * 新增资金策略模板
     * 
     * @param fundTemplate 资金策略模板
     * @return 结果
     */
    public int insertFundTemplate(FundTemplate fundTemplate);

    /**
     * 修改资金策略模板
     * 
     * @param fundTemplate 资金策略模板
     * @return 结果
     */
    public int updateFundTemplate(FundTemplate fundTemplate);

    /**
     * 批量删除资金策略模板
     * 
     * @param ids 需要删除的资金策略模板主键集合
     * @return 结果
     */
    public int deleteFundTemplateByIds(Long[] ids);

    /**
     * 删除资金策略模板信息
     * 
     * @param id 资金策略模板主键
     * @return 结果
     */
    public int deleteFundTemplateById(Long id);
}
