import logging
from typing import TYPE_CHECKING, List, Optional, Sequence

from pysqlcipher3 import dbapi2 as sqlcipher

from rotkehlchen.chain.ethereum.structures import Eth2Validator
from rotkehlchen.chain.ethereum.typing import Eth2Deposit, ValidatorDailyStats
from rotkehlchen.db.utils import form_query_to_filter_timestamps
from rotkehlchen.errors import InputError
from rotkehlchen.logging import RotkehlchenLogsAdapter
from rotkehlchen.typing import ChecksumEthAddress, Timestamp, Union

if TYPE_CHECKING:
    from rotkehlchen.db.dbhandler import DBHandler

ETH2_DEPOSITS_PREFIX = 'eth2_deposits'

logger = logging.getLogger(__name__)
log = RotkehlchenLogsAdapter(logger)


class DBEth2():

    def __init__(self, database: 'DBHandler') -> None:
        self.db = database

    def add_eth2_deposits(self, deposits: Sequence[Eth2Deposit]) -> None:
        """Inserts a list of Eth2Deposit"""
        query = (
            """
            INSERT INTO eth2_deposits (
                tx_hash,
                log_index,
                from_address,
                timestamp,
                pubkey,
                withdrawal_credentials,
                amount,
                usd_value,
                deposit_index
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )
        cursor = self.db.conn.cursor()
        for deposit in deposits:
            deposit_tuple = deposit.to_db_tuple()
            try:
                cursor.execute(query, deposit_tuple)
            except sqlcipher.IntegrityError:  # pylint: disable=no-member
                self.db.msg_aggregator.add_warning(
                    f'Tried to add an ETH2 deposit that already exists in the DB. '
                    f'Deposit data: {deposit_tuple}. Skipping deposit.',
                )
                continue

        self.db.update_last_write()

    def get_eth2_deposits(
            self,
            from_ts: Optional[Timestamp] = None,
            to_ts: Optional[Timestamp] = None,
            address: Optional[ChecksumEthAddress] = None,
    ) -> List[Eth2Deposit]:
        """Returns a list of Eth2Deposit filtered by time and address"""
        cursor = self.db.conn.cursor()
        query = (
            'SELECT '
            'tx_hash, '
            'log_index, '
            'from_address, '
            'timestamp, '
            'pubkey, '
            'withdrawal_credentials, '
            'amount, '
            'usd_value, '
            'deposit_index '
            'FROM eth2_deposits '
        )
        # Timestamp filters are omitted, done via `form_query_to_filter_timestamps`
        filters = []
        if address is not None:
            filters.append(f'from_address="{address}" ')

        if filters:
            query += 'WHERE '
            query += 'AND '.join(filters)

        query, bindings = form_query_to_filter_timestamps(query, 'timestamp', from_ts, to_ts)
        results = cursor.execute(query, bindings)

        return [Eth2Deposit.deserialize_from_db(deposit_tuple) for deposit_tuple in results]

    def add_validator_daily_stats(self, stats: List[ValidatorDailyStats]) -> None:
        """Adds given daily stats for validator in the DB. If an entry exists it's skipped"""
        cursor = self.db.conn.cursor()
        for entry in stats:  # not doing executemany to just ignore existing entry
            try:
                cursor.execute(
                    'INSERT INTO eth2_daily_staking_details('
                    '    validator_index,'
                    '    timestamp,'
                    '    start_usd_price,'
                    '    end_usd_price,'
                    '    pnl,'
                    '    start_amount,'
                    '    end_amount,'
                    '    missed_attestations,'
                    '    orphaned_attestations,'
                    '    proposed_blocks,'
                    '    missed_blocks,'
                    '    orphaned_blocks,'
                    '    included_attester_slashings,'
                    '    proposer_attester_slashings,'
                    '    deposits_number,'
                    '    amount_deposited) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    entry.to_db_tuple(),
                )
            except sqlcipher.IntegrityError:  # pylint: disable=no-member
                log.debug(
                    f'Eth2 staking detail entry {str(entry)} already existed in the DB. Skipping.',
                )

        self.db.update_last_write()

    def get_validator_daily_stats(
            self,
            validator_index: int,
            from_ts: Optional[Timestamp] = None,
            to_ts: Optional[Timestamp] = None,
    ) -> List[ValidatorDailyStats]:
        """Gets all DB entries for daily staking stats of a validator"""
        cursor = self.db.conn.cursor()
        querystr = (
            'SELECT validator_index,'
            '    timestamp,'
            '    start_usd_price,'
            '    end_usd_price,'
            '    pnl,'
            '    start_amount,'
            '    end_amount,'
            '    missed_attestations,'
            '    orphaned_attestations,'
            '    proposed_blocks,'
            '    missed_blocks,'
            '    orphaned_blocks,'
            '    included_attester_slashings,'
            '    proposer_attester_slashings,'
            '    deposits_number,'
            '    amount_deposited '
            '    FROM eth2_daily_staking_details '
            '    WHERE validator_index = ? '
        )
        querystr, bindings = form_query_to_filter_timestamps(
            query=querystr,
            timestamp_attribute='timestamp',
            from_ts=from_ts,
            to_ts=to_ts,
        )
        results = cursor.execute(querystr, (validator_index, *bindings))
        return [ValidatorDailyStats.deserialize_from_db(x) for x in results]

    def validator_exists(self, field: str, arg: Union[int, str]) -> bool:
        cursor = self.db.conn.cursor()
        result = cursor.execute(f'SELECT COUNT(*) from eth2_validators WHERE {field}=?', (arg,))
        return result.fetchone()[0] == 1

    def get_validators(self) -> List[Eth2Validator]:
        cursor = self.db.conn.cursor()
        results = cursor.execute('SELECT * from eth2_validators;')
        return [Eth2Validator.deserialize_from_db(x) for x in results]

    def add_validators(self, validators: List[Eth2Validator]) -> None:
        cursor = self.db.conn.cursor()
        cursor.executemany(
            'INSERT OR IGNORE INTO '
            'eth2_validators(validator_index, public_key) VALUES(?, ?)',
            [x.serialize_for_db() for x in validators],
        )
        self.db.update_last_write()

    def delete_validator(self, validator_index: Optional[int], public_key: Optional[str]) -> None:
        """Deletes the given validator from the DB. Due to marshmallow here at least one
        of the two arguments is not None.

        May raise:
        - InputError if the given validator to delete does not exist in the DB
        """
        cursor = self.db.conn.cursor()
        if validator_index is not None:
            field = 'validator_index'
            input_tuple = (validator_index,)
        else:  # public key can't be None due to marshmallow
            field = 'public_key'
            input_tuple = (public_key,)  # type: ignore

        cursor.execute(f'DELETE FROM eth2_validators WHERE {field} == ?', input_tuple)
        if cursor.rowcount != 1:
            raise InputError(
                f'Tried to delete eth2 validator with {field} '
                f'{input_tuple[0]} from the DB but it did not exist',
            )
        self.db.update_last_write()
