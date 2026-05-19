package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.FundTemplate;

/**
 * 资金策略模板Mapper接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface FundTemplateMapper 
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
     * 删除资金策略模板
     * 
     * @param id 资金策略模板主键
     * @return 结果
     */
    public int deleteFundTemplateById(Long id);

    /**
     * 批量删除资金策略模板
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteFundTemplateByIds(Long[] ids);
}
