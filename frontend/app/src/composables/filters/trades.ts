import { type ComputedRef, type Ref } from 'vue';
import { z } from 'zod';
import {
  type MatchedKeyword,
  type SearchMatcher,
  assetDeTransformer,
  assetSuggestions,
  dateDeTransformer,
  dateTransformer,
  dateValidator
} from '@/types/filtering';
import { TradeType } from '@/types/history/trade';
import { getDateInputISOFormat } from '@/utils/date';

enum TradeFilterKeys {
  BASE = 'base',
  QUOTE = 'quote',
  ACTION = 'action',
  START = 'start',
  END = 'end',
  LOCATION = 'location'
}

enum TradeFilterValueKeys {
  BASE = 'baseAsset',
  QUOTE = 'quoteAsset',
  ACTION = 'tradeType',
  START = 'fromTimestamp',
  END = 'toTimestamp',
  LOCATION = 'location'
}

type Matcher = SearchMatcher<TradeFilterKeys, TradeFilterValueKeys>;
type Filters = MatchedKeyword<TradeFilterValueKeys>;

export const useTradeFilters = () => {
  const filters: Ref<Filters> = ref({});

  const { associatedLocations } = storeToRefs(useAssociatedLocationsStore());
  const { dateInputFormat } = storeToRefs(useFrontendSettingsStore());
  const { assetSearch } = useAssetInfoApi();
  const { assetInfo } = useAssetInfoRetrievalStore();
  const { tc } = useI18n();

  const matchers: ComputedRef<Matcher[]> = computed(() => [
    {
      key: TradeFilterKeys.BASE,
      keyValue: TradeFilterValueKeys.BASE,
      description: tc('closed_trades.filter.base_asset'),
      asset: true,
      suggestions: assetSuggestions(assetSearch),
      deTransformer: assetDeTransformer(assetInfo)
    },
    {
      key: TradeFilterKeys.QUOTE,
      keyValue: TradeFilterValueKeys.QUOTE,
      description: tc('closed_trades.filter.quote_asset'),
      asset: true,
      suggestions: assetSuggestions(assetSearch),
      deTransformer: assetDeTransformer(assetInfo)
    },
    {
      key: TradeFilterKeys.ACTION,
      keyValue: TradeFilterValueKeys.ACTION,
      description: tc('closed_trades.filter.trade_type'),
      string: true,
      suggestions: () => TradeType.options,
      validate: type => (TradeType.options as string[]).includes(type)
    },
    {
      key: TradeFilterKeys.START,
      keyValue: TradeFilterValueKeys.START,
      description: tc('closed_trades.filter.start_date'),
      string: true,
      suggestions: () => [],
      hint: tc('closed_trades.filter.date_hint', 0, {
        format: getDateInputISOFormat(get(dateInputFormat))
      }),
      validate: dateValidator(dateInputFormat),
      transformer: dateTransformer(dateInputFormat),
      deTransformer: dateDeTransformer(dateInputFormat)
    },
    {
      key: TradeFilterKeys.END,
      keyValue: TradeFilterValueKeys.END,
      description: tc('closed_trades.filter.end_date'),
      string: true,
      suggestions: () => [],
      hint: tc('closed_trades.filter.date_hint', 0, {
        format: getDateInputISOFormat(get(dateInputFormat))
      }),
      validate: dateValidator(dateInputFormat),
      transformer: dateTransformer(dateInputFormat),
      deTransformer: dateDeTransformer(dateInputFormat)
    },
    {
      key: TradeFilterKeys.LOCATION,
      keyValue: TradeFilterValueKeys.LOCATION,
      description: tc('closed_trades.filter.location'),
      string: true,
      suggestions: () => get(associatedLocations),
      validate: location => get(associatedLocations).includes(location as any)
    }
  ]);

  const updateFilter = (newFilters: Filters) => {
    set(filters, newFilters);
  };

  const OptionalString = z.string().optional();
  const RouteFilterSchema = z.object({
    [TradeFilterValueKeys.BASE]: OptionalString,
    [TradeFilterValueKeys.QUOTE]: OptionalString,
    [TradeFilterValueKeys.ACTION]: OptionalString,
    [TradeFilterValueKeys.START]: OptionalString,
    [TradeFilterValueKeys.END]: OptionalString,
    [TradeFilterValueKeys.LOCATION]: OptionalString
  });

  return {
    filters,
    matchers,
    updateFilter,
    RouteFilterSchema
  };
};
