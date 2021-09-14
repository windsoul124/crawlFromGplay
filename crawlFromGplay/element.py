from typing import Callable, List, Any, Optional


def nested_lookup(source, indexes):
    if len(indexes) == 1:
        return source[indexes[0]]
    return nested_lookup(source[indexes[0]], indexes[1::])

class ElementSpec:
    def __init__(
        self,
        ds_num: Optional[int],
        data_map: List[int],
        post_processor: Callable = None,
        fallback_value: Any = None,
    ):
        self.ds_num = ds_num
        self.data_map = data_map
        self.post_processor = post_processor
        self.fallback_value = fallback_value

    def extract_content(self, source: dict) -> Any:
        try:
            if self.ds_num is None:
                result = nested_lookup(source, self.data_map)
            else:
                result = nested_lookup(
                    source["ds:{}".format(self.ds_num)], self.data_map
                )

            if self.post_processor is not None:
                result = self.post_processor(result)
        except:
            if isinstance(self.fallback_value, ElementSpec):
                result = self.fallback_value.extract_content(source)
            else:
                result = self.fallback_value

        return result

class ElementSpecs:

    Permission_Type = ElementSpec(None, [0])
    Permission_List = ElementSpec(
        None, [2], lambda container: sorted([item[1] for item in container])
    )
